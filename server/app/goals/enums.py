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


class GoalRefillRuleEnum(models.TextChoices):
    """Справочник условий Целей накопления"""

    gt = "Больше"
    gte = "Больше или равно"
    eq = "Равно"  # Нужно ли??


# Собираем вручную уникальные значения возможных Целей пользователя
UNIQUE_GOAL_ENUMS = [
    (each_item.name, each_item.value) for each_item in BudgetRuleEnum  # type: ignore
] + [
    (each_item.name, each_item.value)
    for each_item in GoalRefillRuleEnum  # type: ignore
    if each_item != GoalRefillRuleEnum.eq
]


# https://github.com/typeddjango/django-stubs/issues/729
GoalRuleEnum = models.TextChoices(  # type: ignore
    "GoalRuleEnum",
    UNIQUE_GOAL_ENUMS,
)
