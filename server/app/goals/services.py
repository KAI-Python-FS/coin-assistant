from typing import Any

from django.db.models.query import QuerySet

from django.db.models import Q
from django.core.exceptions import ValidationError

from server.app.base.services import BaseModelUserFilterCRUDService

from .enums import GoalTypeEnum
from .models import Goal


class GoalRefillService(BaseModelUserFilterCRUDService):
    """Класс описания бизнес логики работы с Целями пользователей"""

    model = Goal

    def _get_qs_retrieve_single(self, object_id: int) -> QuerySet:
        """Возвращает кварисет получения конкретной записи объекта"""
        qs_filters = self._filters_retrieve_single(object_id)

        return self.model.objects.goals().filter(qs_filters)

    def _get_qs_retrieve_list(self, **filters) -> QuerySet:
        """Возвращает кварисет получения списка записей объекта"""
        qs_filters = self._filters_retrieve_list(**filters)

        return self.model.objects.goals().filter(qs_filters).all()

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает условия фильтрации получения списка объектов"""
        base_filters = super()._filters_retrieve_list(**filters)

        filter_condition = Q()
        filter_condition.add(base_filters, Q.AND)

        for each_filter_key, each_filter_value in filters.items():
            match each_filter_key:
                # FIXME сейчас нельзя отфильтроваться по Целям без категорий
                case "by_categories":
                    filter_condition.add(
                        Q(category_id__in=each_filter_value),
                        Q.AND,
                    )
                case "by_state":
                    filter_condition.add(
                        Q(state=each_filter_value),
                        Q.AND,
                    )
                case "by_start_date":
                    filter_condition.add(
                        Q(start_date__gte=each_filter_value),
                        Q.AND,
                    )
                case "by_finish_date":
                    filter_condition.add(
                        Q(finish_date__lte=each_filter_value),
                        Q.AND,
                    )
                case "by_budget_rule":
                    filter_condition.add(
                        Q(rule=each_filter_value),
                        Q.AND,
                    )
                case _:
                    raise Exception("Неизвестный фильтр")

        return filter_condition

    def create(self, **object_data) -> Goal:
        """Создание объекта"""
        # TODO возможно стоит вынести в родительский метод разбор является ли переданное поле FK
        raw_category = object_data.get("category")
        if raw_category is not None and isinstance(raw_category, int):
            object_data.pop("category")
            object_data["category_id"] = raw_category

        object_data.update({
            "goal_type": GoalTypeEnum.REFILL.value,
        })

        return super().create(**object_data)  # type: ignore

    def update(self, object_id: int, **object_data: dict) -> Goal | None:
        """Обновление объекта"""
        ready_to_update_fields = [
            "name",
            "description",
            "category",
            "start_date",
            "finish_date",
            "value",
            "state",
            "rule",
        ]

        fields_diff = set(object_data.keys()) - set(ready_to_update_fields)
        if fields_diff:
            raise ValidationError(f"Переданы поля {fields_diff}, недоступные к обновлению")

        return super().update(object_id, **object_data)


class BudgetService(BaseModelUserFilterCRUDService):
    """Класс описания бизнес логики работы с Бюджетами пользователей"""

    model = Goal

    def _get_qs_retrieve_single(self, object_id: int) -> QuerySet:
        """Возвращает кварисет получения конкретной записи объекта"""
        qs_filters = self._filters_retrieve_single(object_id)

        return self.model.objects.budgets().filter(qs_filters)

    def _get_qs_retrieve_list(self, **filters) -> QuerySet:
        """Возвращает кварисет получения списка записей объекта"""
        qs_filters = self._filters_retrieve_list(**filters)

        return self.model.objects.budgets().filter(qs_filters).all()

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает условия фильтрации получения списка объектов"""
        base_filters = super()._filters_retrieve_list(**filters)

        filter_condition = Q()
        filter_condition.add(base_filters, Q.AND)

        for each_filter_key, each_filter_value in filters.items():
            match each_filter_key:
                case "by_categories":
                    filter_condition.add(
                        Q(category_id__in=each_filter_value),
                        Q.AND,
                    )
                case "by_state":
                    filter_condition.add(
                        Q(state=each_filter_value),
                        Q.AND,
                    )
                case "by_start_date":
                    filter_condition.add(
                        Q(start_date__gte=each_filter_value),
                        Q.AND,
                    )
                case "by_finish_date":
                    filter_condition.add(
                        Q(finish_date__lte=each_filter_value),
                        Q.AND,
                    )
                case "by_budget_rule":
                    filter_condition.add(
                        Q(rule=each_filter_value),
                        Q.AND,
                    )
                case _:
                    raise Exception("Неизвестный фильтр")

        return filter_condition

    def create(self, *args, **object_data: dict[str, Any]) -> Goal:
        """Создание объекта"""
        # TODO возможно стоит вынести в родительский метод разбор является ли переданное поле FK
        raw_category = object_data.get("category")
        if raw_category is not None and isinstance(raw_category, int):
            object_data.pop("category")
            object_data["category_id"] = raw_category

        object_data.update({
            "goal_type": GoalTypeEnum.SPENDING.value,
        })

        return super().create(*args, **object_data)  # type: ignore

    def update(self, object_id: int, **object_data: dict) -> Goal | None:
        """Обновление объекта"""
        ready_to_update_fields = [
            "name",
            "description",
            "category",
            "start_date",
            "finish_date",
            "value",
            "state",
            "rule",
        ]

        fields_diff = set(object_data.keys()) - set(ready_to_update_fields)
        if fields_diff:
            raise ValidationError(f"Переданы поля {fields_diff}, недоступные к обновлению")

        return super().update(object_id, **object_data)
