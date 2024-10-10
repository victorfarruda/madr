from http import HTTPStatus


def test_create_novelist(client, token):
    response = client.post(
        '/novelists', headers={'Authorization': f'Bearer {token}'}, json={'name': 'Clarice Lispector'}
    )

    assert HTTPStatus.CREATED == response.status_code
    assert {'name': 'Clarice Lispector', 'id': 1} == response.json()


def test_create_novelist_should_return_unauthorized(client):
    response = client.post('/novelists', json={'name': 'Clarice Lispector'})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_get_all_novelists(client, novelists_10, token):
    objects_quantity = 10
    response = client.get('/novelists', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert HTTPStatus.OK == response.status_code
    assert objects_quantity == len(json_response.get('novelists'))


def test_get_all_novelists_should_return_unauthorized(client):
    response = client.get('/novelists')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_patch_novelist(client, novelist, token):
    response = client.patch(
        f'/novelists/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Algum nome de romancista'},
    )

    assert HTTPStatus.OK == response.status_code
    assert {'name': 'Algum nome de romancista', 'id': novelist.id} == response.json()


def test_patch_novelist_should_return_not_found(client, novelist, token):
    response = client.patch(
        '/novelists/951', headers={'Authorization': f'Bearer {token}'}, json={'name': 'Algum nome de romancista'}
    )

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_patch_novelist_should_return_unauthorized(client, novelist):
    response = client.patch(
        f'/novelists/{novelist.id}',
        json={'name': 'Algum nome de romancista'},
    )

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_get_novelist(client, novelist, token):
    response = client.get(f'/novelists/{novelist.id}', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.OK == response.status_code
    assert {'id': novelist.id, 'name': novelist.name} == response.json()


def test_get_novelist_should_return_not_found(client, token):
    response = client.get('/novelists/987', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_get_novelist_should_return_unauthorized(client, novelist):
    response = client.get(f'/novelists/{novelist.id}')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_delete_novelist(client, novelist, token):
    response = client.delete(f'/novelists/{novelist.id}', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.OK == response.status_code
    assert {'message': 'Novelist has been deleted successfully.'} == response.json()


def test_delete_novelist_should_return_not_found(client, token):
    response = client.delete('/novelists/753', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_delete_novelist_should_return_unauthorized(client, novelist):
    response = client.delete(f'/novelists/{novelist.id}')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()
