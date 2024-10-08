from http import HTTPStatus


def test_create_book_should_create_a_book(client, novelist):
    response = client.post('/books', json={'title': 'Algum título', 'novelist_id': novelist.id, 'year': 2024})

    assert HTTPStatus.CREATED == response.status_code
    assert {'id': 1, 'title': 'Algum título', 'novelist_id': novelist.id, 'year': 2024} == response.json()


def test_create_book_should_raise_exception_novelist_does_not_exist(client, novelist):
    response = client.post('/books', json={'title': 'Algum título', 'novelist_id': 963, 'year': 2024})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_get_all_books(client, books_10):
    quantity_books = 10
    response = client.get('/books')

    json_response = response.json()

    assert HTTPStatus.OK == response.status_code
    assert quantity_books == len(json_response.get('books'))


def test_patch_book_should_update_a_book(client, book):
    response = client.patch(f'/books/{book.id}', json={'title': 'Meu novo titulo'})

    assert HTTPStatus.OK == response.status_code
    assert {
        'id': book.id,
        'title': 'Meu novo titulo',
        'novelist_id': book.novelist_id,
        'year': book.year,
    } == response.json()


def test_patch_book_should_raise_book_not_found(client):
    response = client.patch('/books/987', json={'title': 'Meu novo titulo'})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()


def test_patch_book_should_raise_novelist_not_found(client):
    response = client.patch('/books/987', json={'title': 'Meu novo titulo', 'novelist_id': 100})

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Novelist not found.'} == response.json()


def test_get_book_should_return_a_book(client, book):
    response = client.get(f'/books/{book.id}')

    assert HTTPStatus.OK == response.status_code
    assert {
        'id': book.id,
        'title': book.title,
        'novelist_id': book.novelist_id,
        'year': book.year,
    } == response.json()


def test_get_book_should_raise_an_exception(client):
    response = client.get('/books/951')

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()


def test_delete_book_should_delete_a_book(client, book):
    response = client.delete(f'/books/{book.id}')

    assert HTTPStatus.OK == response.status_code
    assert {'message': 'Book has been deleted successfully.'} == response.json()


def test_delete_book_should_raise_an_exception(client):
    response = client.delete('/books/951')

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert {'detail': 'Book not found.'} == response.json()
