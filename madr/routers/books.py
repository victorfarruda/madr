from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book
from madr.schemas import BookSchema

router = APIRouter(prefix='/books', tags=['books'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.OK, response_model=BookSchema)
def create_book(book: BookSchema, session: T_Session):
    db_todo: Book = Book(
        year=book.year,
        title=book.title,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
