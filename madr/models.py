from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = 'novelists'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]

    books: Mapped[list['Book']] = relationship(init=False, back_populates='novelist', cascade='all, delete-orphan')


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    title: Mapped[str]
    year: Mapped[int]
    novelist_id: Mapped[int] = mapped_column(ForeignKey('novelists.id'))

    novelist: Mapped['Novelist'] = relationship(init=False, back_populates='books')
