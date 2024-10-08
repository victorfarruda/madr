from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book, Novelist
from madr.schemas import BookList, BookPublic, BookSchema, BookUpdate, Message

router = APIRouter(prefix='/books', tags=['books'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.OK, response_model=BookPublic)
def create_book(book: BookSchema, session: T_Session):
    db_novelist = session.scalar(select(Novelist).where(Novelist.id == book.novelist_id))

    if not db_novelist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Novelist not found.')

    db_book: Book = Book(
        year=book.year,
        title=book.title,
        novelist_id=book.novelist_id,
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/', status_code=HTTPStatus.OK, response_model=BookList)
def get_all_books(session: T_Session):
    books = session.scalars(select(Book)).all()
    return {'books': books}


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(book_id: int, session: T_Session, book: BookUpdate):
    if book.novelist_id is not None:
        db_novelist = session.scalar(select(Novelist).where(Novelist.id == book.novelist_id))

        if not db_novelist:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Novelist not found.')

    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Book not found.')

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/{book_id}', response_model=BookPublic)
def get_book(book_id: int, session: T_Session):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Book not found.')

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: T_Session):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Book not found.')

    session.delete(db_book)
    session.commit()

    return {'message': 'Book has been deleted successfully.'}
