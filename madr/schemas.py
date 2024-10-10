from pydantic import BaseModel


class Message(BaseModel):
    message: str


class BookSchema(BaseModel):
    year: int
    title: str
    novelist_id: int


class BookPublic(BookSchema):
    id: int


class BookList(BaseModel):
    books: list[BookPublic]


class BookUpdate(BaseModel):
    year: int | None = None
    title: str | None = None
    novelist_id: int | None = None


class NovelistSchema(BaseModel):
    name: str


class NovelistPublic(NovelistSchema):
    id: int


class NovelistList(BaseModel):
    novelists: list[NovelistPublic]


class NovelistUpdate(BaseModel):
    name: str | None = None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool
