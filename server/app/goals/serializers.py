import datetime

from pydantic import BaseModel

from .enums import GoalRuleEnum, GoalStateEnum, GoalTypeEnum


class BaseGoalSerializer(BaseModel):
    """Схема данных одной операции"""

    name: str
    description: str | None
    # goal_type: GoalTypeEnum
    category: str
    start_date: datetime.date
    finish_date: datetime.date | None
    state: GoalStateEnum
    value: float | None
    rule: GoalRuleEnum


class GoalListItemOutputSerializer(BaseGoalSerializer):
    """Схема исходящих данных одной цели накопления пользователя"""
