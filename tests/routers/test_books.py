from http import HTTPStatus


def test_create_book_should_create_a_book(client, novelist, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Algum título', 'novelist_id': novelist.id, 'year': 2024},
    )

    assert HTTPStatus.CREATED == response.status_code
    assert {'id': 1, 'title': 'Algum título', 'novelist_id': novelist.id, 'year': 2024} == response.json()


def test_create_book_should_raise_exception_novelist_does_not_exist(client, novelist, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Algum título', 'novelist_id': 963, 'year': 2024},
    )

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_create_book_should_return_unauthorized(client, novelist):
    response = client.post(
        '/books',
        json={'title': 'Algum título', 'novelist_id': novelist.id, 'year': 2024},
    )

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_get_all_books(client, books_10, token):
    quantity_books = 10
    response = client.get('/books', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert HTTPStatus.OK == response.status_code
    assert quantity_books == len(json_response.get('books'))


def test_get_all_books_should_return_unauthorized(client, novelist):
    response = client.get('/books')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_patch_book_should_update_a_book(client, book, token):
    response = client.patch(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Meu novo titulo'}
    )

    assert HTTPStatus.OK == response.status_code
    assert {
        'id': book.id,
        'title': 'Meu novo titulo',
        'novelist_id': book.novelist_id,
        'year': book.year,
    } == response.json()


def test_patch_book_should_raise_book_not_found(client, token):
    response = client.patch(
        '/books/987', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Meu novo titulo'}
    )

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()


def test_patch_book_should_raise_novelist_not_found(client, token):
    response = client.patch(
        '/books/987',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Meu novo titulo', 'novelist_id': 100},
    )

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_patch_book_should_return_unauthorized(client, novelist, book):
    response = client.patch(f'/books/{book.id}', json={'title': 'Meu novo titulo'})

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_get_book_should_return_a_book(client, book, token):
    response = client.get(f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.OK == response.status_code
    assert {
        'id': book.id,
        'title': book.title,
        'novelist_id': book.novelist_id,
        'year': book.year,
    } == response.json()


def test_get_book_should_raise_an_exception(client, token):
    response = client.get('/books/951', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()


def test_get_book_should_return_unauthorized(client, novelist, book):
    response = client.get(f'/books/{book.id}')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()


def test_delete_book_should_delete_a_book(client, book, token):
    response = client.delete(f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.OK == response.status_code
    assert {'message': 'Book has been deleted successfully.'} == response.json()


def test_delete_book_should_raise_an_exception(client, token):
    response = client.delete('/books/951', headers={'Authorization': f'Bearer {token}'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()


def test_delete_book_should_return_unauthorized(client, novelist, book):
    response = client.delete(f'/books/{book.id}')

    assert HTTPStatus.UNAUTHORIZED == response.status_code
    assert {'detail': 'Not authenticated'} == response.json()
