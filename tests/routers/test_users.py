from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
            'full_name': 'Alice Freitas',
            'disabled': True,
        },
    )
    assert HTTPStatus.CREATED == response.status_code
    assert {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
        'full_name': 'Alice Freitas',
        'disabled': True,
    } == response.json()


def test_create_user_with_an_existent_username(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
            'full_name': 'Alice Freitas',
            'disabled': True,
        },
    )
    assert HTTPStatus.BAD_REQUEST == response.status_code
    assert {'detail': 'Username already exists'} == response.json()


def test_create_user_with_an_existent_email(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'userteste123',
            'email': user.email,
            'password': 'secret',
            'full_name': 'Alice Freitas',
            'disabled': True,
        },
    )
    assert HTTPStatus.BAD_REQUEST == response.status_code
    assert {'detail': 'Email already exists'} == response.json()


def test_get_current_user(client, user, token):
    response = client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    response_json = response.json()
    assert HTTPStatus.OK == response.status_code
    assert 'id' in response_json
    assert 'username' in response_json
    assert 'email' in response_json
    assert 'full_name' in response_json
    assert 'disabled' in response_json


def test_patch_user(client, user, token):
    response = client.patch(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert {
        'username': user.username,
        'email': 'bob@example.com',
        'full_name': user.full_name,
        'disabled': False,
        'id': user.id,
    } == response.json()
