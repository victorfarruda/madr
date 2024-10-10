import factory

from madr.models import Book, Novelist, User


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


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'usernametest{n}')
    full_name = factory.Faker('name')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    hashed_password = factory.LazyAttribute(lambda obj: f'{obj.username}+pass')
    disabled = False
