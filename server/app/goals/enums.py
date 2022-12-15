
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


class GoalRuleEnum(models.TextChoices):
    """Справочник условия достижения цели"""

    lt = "Меньше"
    lte = "Меньше или равно"
    gt = "Больше"
    gte = "Больше или равно"
    eq = "Равно"
