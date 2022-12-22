import datetime

from pydantic import BaseModel

from server.app.operations.serializers import BaseCategorySerializer

from . import enums


class BaseGoalCategorySerializer(BaseCategorySerializer):
    """Сериализатор данных о категории"""


class BaseGoalSerializer(BaseModel):
    """Сериализатор данных одной операции"""

    id: int
    name: str
    description: str | None
    category: BaseGoalCategorySerializer | None
    start_date: datetime.date
    finish_date: datetime.date | None
    state: enums.GoalStateEnum
    value: float | None
    rule: enums.GoalRefillEnum

    class Config:
        orm_mode = True


class GoalRefillListFilterSerializer(BaseModel):
    """Сериализатор фильтров получения списка Целей накопления пользователя"""

    by_categories: list[int] | None
    by_state: enums.GoalStateEnum | None
    by_start_date: datetime.date | None
    by_finish_date: datetime.date | None
    by_goal_rule: enums.GoalRefillEnum | None


class GoalRefillListItemOutputSerializer(BaseGoalSerializer):
    """Сериализатор исходящих данных одной цели накопления пользователя"""


class GoalRefillCreateInputSerializer(BaseModel):
    """Сериализатор входящих данных создания Цели накопления пользователя"""

    name: str
    description: str | None
    category: int | None
    start_date: datetime.date
    finish_date: datetime.date | None
    state: enums.GoalStateEnum
    value: float | None
    rule: enums.GoalRefillEnum


class GoalRefillCreateOutputSerializer(BaseGoalSerializer):
    """Сериализатор исходящих данных создания Цели накопления пользователя"""
