from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Purchase(models.Model):
    """Модель покупки"""

    name = models.TextField(
        verbose_name="Наименование покупки",
    )
    description = models.TextField(
        null=True,
        verbose_name="Описание покупки",
    )
    purchased_at = models.DateTimeField(
        verbose_name="Дата покупки",
    )
    cost = models.FloatField(
        verbose_name="Стоимость",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.user}-at-{self.purchased_at}'
