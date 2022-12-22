from typing import Any

from django.db.models.query import QuerySet

from server.app.base.services import BaseModelUserFilterCRUDService

from .enums import GoalTypeEnum
from .models import Goal


class GoalRefillService(BaseModelUserFilterCRUDService):
    """Класс описания бизнес логики работы с Целями пользователей"""

    model = Goal

    def _get_qs_retrieve_single(self, object_id: int) -> QuerySet:
        """Возвращает кварисет получения конкретной записи объекта"""
        qs_filters = self._filters_retrieve_single(object_id)

        return self.model.objects.goals.filter(qs_filters)

    def _get_qs_retrieve_list(self, **filters) -> QuerySet:
        """Возвращает кварисет получения списка записей объекта"""
        qs_filters = self._filters_retrieve_list(**filters)

        return self.model.objects.goals.filter(qs_filters).all()

    def create(self, *args, **object_data: dict[str, Any]) -> Goal:
        """Создание объекта"""
        # TODO возможно стоит вынести в родительский метод разбор является ли переданное поле FK
        raw_category = object_data.get("category")
        if raw_category is not None and isinstance(raw_category, int):
            object_data.pop("category")
            object_data["category_id"] = raw_category

        object_data.update({
            "goal_type": GoalTypeEnum.REFILL.value,
        })

        return super().create(*args, **object_data)  # type: ignore
