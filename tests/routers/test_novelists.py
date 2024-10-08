from http import HTTPStatus


def test_create_novelist(client):
    response = client.post('/novelists', json={'name': 'Clarice Lispector'})

    assert {'name': 'Clarice Lispector', 'id': 1} == response.json()


def test_get_all_novelists(client, novelists_10):
    objects_quantity = 10
    response = client.get('/novelists')

    json_response = response.json()

    assert objects_quantity == len(json_response.get('novelists'))


def test_patch_novelist(client, novelist):
    response = client.patch(f'/novelists/{novelist.id}', json={'name': 'Algum nome de romancista'})

    assert {'name': 'Algum nome de romancista', 'id': novelist.id} == response.json()


def test_patch_novelist_should_return_not_found(client, novelist):
    response = client.patch('/novelists/951', json={'name': 'Algum nome de romancista'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_get_novelist(client, novelist):
    response = client.get(f'/novelists/{novelist.id}')

    assert {
        'id': novelist.id,
        'name': novelist.name,
    } == response.json()


def test_get_novelist_should_return_not_found(client):
    response = client.get('/novelists/987')

    assert {'detail': 'Novelist not found.'} == response.json()


def test_delete_novelist(client, novelist):
    response = client.delete(f'/novelists/{novelist.id}')

    assert {'message': 'Novelist has been deleted successfully.'} == response.json()


def test_delete_novelist_should_return_not_found(client):
    response = client.delete('/novelists/753')

    assert {'detail': 'Novelist not found.'} == response.json()
