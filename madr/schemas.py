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


class NovelistSchema(BaseModel):
    name: str


class NovelistPublic(NovelistSchema):
    id: int


class NovelistList(BaseModel):
    novelists: list[NovelistPublic]


class NovelistUpdate(BaseModel):
    name: str | None = None
