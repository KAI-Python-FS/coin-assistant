from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from .enums import OperationTypeEnum
from .validation import validate_operation_cost

User = get_user_model()


class Category(models.Model):
    """Модель категории покупки"""

    name = models.CharField(max_length=64, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Operation(models.Model):
    """Модель операции"""

    name = models.TextField(
        verbose_name="Наименование операции",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание операции",
    )
    operation_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="Дата операции",
    )
    operation_type = models.CharField(
        verbose_name="Тип операции",
        choices=OperationTypeEnum.choices,
        max_length=64,
    )
    cost = models.FloatField(
        verbose_name="Стоимость",
        validators=[validate_operation_cost],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name="Покупатель",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name="Категория операции",
    )

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self):
        return f"{self.user}-at-{self.operation_at}-{self.name}"
