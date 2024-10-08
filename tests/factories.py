import factory

from madr.models import Book, Novelist


class NovelistFactory(factory.Factory):
    class Meta:
        model = Novelist

    name = factory.Faker('name')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Faker('text')
    year = factory.Faker('pyint')
    novelist_id = 1
