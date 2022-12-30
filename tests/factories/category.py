import factory

from factory.django import DjangoModelFactory

from server.app.operations.models import Category


class CategoryFactory(DjangoModelFactory):
    """Фабрика создания категорий"""

    name = factory.Sequence(lambda n: f'Категория {n}')

    class Meta:
        model = Category
