from http import HTTPStatus

from freezegun import freeze_time

from madr.security import create_access_token


def test_login_for_access_token(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})
    response_json = response.json()

    assert HTTPStatus.OK == response.status_code
    assert 'access_token' in response_json
    assert 'token_type' in response_json


def test_login_for_access_token_should_return_user_or_password_incorrect_password(client, user):
    response = client.post('/auth/token', data={'username': 'user', 'password': user.clean_password})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Incorrect username or password'} == response.json()


def test_login_for_access_token_should_return_user_or_password_incorrect_username(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': 'pass'})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Incorrect username or password'} == response.json()


def test_token_expired_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.username, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.patch(
            '/users/me',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token_should_a_new_token(client, token):
    response = client.post('/auth/refresh-token', headers={'Authorization': f'Bearer {token}'})
    response_json = response.json()

    assert HTTPStatus.OK == response.status_code
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response_json
    assert 'token_type' in response_json
    assert response_json['token_type'] == 'bearer'


def test_refresh_token_should_return_not_authenticated(client):
    response = client.post('/auth/refresh-token')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_authorization_when_user_is_deleted(client, session, token, user):
    session.delete(user)
    session.commit()

    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Could not validate credentials'} == response.json()


def test_authorization_when_user_is_disabled(client, session, token, user):
    user.disabled = True
    session.add(user)
    session.commit()

    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.BAD_REQUEST == response.status_code
    assert {'detail': 'Inactive user'} == response.json()


def test_authorization_when_user_is_none(client, session):
    token = create_access_token(data={'sub': None})

    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Could not validate credentials'} == response.json()
