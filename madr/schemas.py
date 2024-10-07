from pydantic import BaseModel


class Message(BaseModel):
    message: str


class BookSchema(BaseModel):
    year: int
    title: str


class BookPublic(BookSchema):
    id: int


class BookList(BaseModel):
    books: list[BookPublic]


class BookUpdate(BaseModel):
    year: int | None = None
    title: str | None = None
