from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Goal(models.Model):
    """Модель Цели"""

    name = models.CharField(
        max_length=255,
        verbose_name="Название цели"
    )
    user = models.ManyToManyField(
        User,
        verbose_name="Покупатель",
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"
