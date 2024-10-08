import factory

from madr.models import Novelist


class NovelistFactory(factory.Factory):
    class Meta:
        model = Novelist

    name = factory.Faker('text')
