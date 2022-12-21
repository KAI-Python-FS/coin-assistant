
from django.db.models.query import QuerySet

from server.app.base.services import BaseModelUserFilterCRUDService
from .models import Goal


class GoalService(BaseModelUserFilterCRUDService):
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
