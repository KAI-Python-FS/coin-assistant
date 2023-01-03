import datetime

import factory
import factory.fuzzy

from factory.django import DjangoModelFactory
from pytz import UTC

from server.app.operations.enums import OperationTypeEnum
from server.app.operations.models import Operation

from .category import CategoryFactory
from .user import UserFactory


class OperationFactory(DjangoModelFactory):
    """Базовая фабрика модели Операция пользователя"""

    name = factory.Sequence(lambda n: f"name_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    operation_at = factory.fuzzy.FuzzyDateTime(  # type: ignore
        datetime.datetime(2020, 1, 1, tzinfo=UTC)
    )
    operation_type = factory.fuzzy.FuzzyChoice(OperationTypeEnum)
    cost = factory.fuzzy.FuzzyFloat(
        0.1,
        10**7,
    )
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Operation
