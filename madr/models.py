from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    title: Mapped[str]
    year: Mapped[int]
