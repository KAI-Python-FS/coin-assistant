import datetime

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from server.app.goals.enums import (
    BudgetRuleEnum,
    GoalRefillRuleEnum,
    GoalStateEnum,
    GoalTypeEnum,
)
from server.app.goals.models import Goal

from .category import CategoryFactory
from .user import UserFactory


class BaseGoalFactory(DjangoModelFactory):
    """Базовая фабрика модели Цели пользователя"""

    name = factory.Sequence(lambda n: f"name_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)
    start_date = factory.fuzzy.FuzzyDateTime(  # type: ignore
        datetime.datetime(2020, 1, 1, tzinfo=UTC)
    )
    finish_date = factory.LazyAttribute(
        lambda o: o.start_date + datetime.timedelta(days=60),
    )
    value = factory.fuzzy.FuzzyFloat(  # type: ignore
        0.1,
        10**7,
    )
    state = GoalStateEnum.unknown

    class Meta:
        model = Goal
        abstract = True


class BudgetFactory(BaseGoalFactory):
    """Фабрика создания бюджета пользователя"""

    goal_type = GoalTypeEnum.SPENDING
    rule = factory.fuzzy.FuzzyChoice(BudgetRuleEnum)

    class Meta:
        model = Goal


class GoalRefillFactory(BaseGoalFactory):
    """Фабрика создания целей накопления пользователя"""

    goal_type = GoalTypeEnum.REFILL
    rule = factory.fuzzy.FuzzyChoice(GoalRefillRuleEnum)

    class Meta:
        model = Goal
