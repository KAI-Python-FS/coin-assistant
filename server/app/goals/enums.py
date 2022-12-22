
from django.db import models


class GoalTypeEnum(models.TextChoices):
    """Справочник типа цели"""

    SPENDING = "Трата"
    REFILL = "Пополнение"


class GoalStateEnum(models.TextChoices):
    """Справочник состояния цели"""

    succeed = "Успешно выполнена"
    failed = "Не выполнена"
    working = "В процессе"
    unknown = "Неизвестно"


class BudgetRuleEnum(models.TextChoices):
    """Справочник условий Бюджета"""
    lt = "Меньше"
    lte = "Меньше или равно"
    eq = "Равно"  # Нужно ли??


class GoalAccumulationEnum(models.TextChoices):
    """Справочник условий Целей накопления"""

    gt = "Больше"
    gte = "Больше или равно"
    eq = "Равно"  # Нужно ли??


class GoalRuleEnum(BudgetRuleEnum, GoalAccumulationEnum):
    """Справочник условия достижения цели"""

    lt = "Меньше"
    lte = "Меньше или равно"
    gt = "Больше"
    gte = "Больше или равно"
    eq = "Равно"  # Нужно ли??
