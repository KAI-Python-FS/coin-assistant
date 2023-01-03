from django.db import models


class OperationTypeEnum(models.TextChoices):
    """Справочник типа операций"""

    SPENDING = "Трата"
    REFILL = "Пополнение"
