from typing import Any

from django.db.models import Q

from server.app.base.services import BaseModelCRUDService, BaseModelUserFilterCRUDService

from .models import Category, Operation


class CategoryService(BaseModelCRUDService):
    """Класс описания бизнес логики работы с Категориями покупок"""

    model = Category


class OperationService(BaseModelUserFilterCRUDService):
    """Класс описания бизнес логики работы с Операциями пользователя"""

    model = Operation

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает список Операций пользователя"""
        filter_condition = Q()

        base_filters = super()._filters_retrieve_list(**filters)
        filter_condition.add(base_filters, Q.AND)

        for each_filter_key, each_filter_value in filters.items():
            match each_filter_key:
                case "by_operation_type":
                    filter_condition.add(
                        Q(operation_type=each_filter_value),
                        Q.AND
                    )
                case "by_categories":
                    filter_condition.add(
                        Q(category_id__in=each_filter_value),
                        Q.AND
                    )
                case "by_operation_start_date":
                    filter_condition.add(
                        Q(operation_at__gte=each_filter_value),
                        Q.AND
                    )
                case "by_operation_finish_date":
                    filter_condition.add(
                        Q(operation_at__lte=each_filter_value),
                        Q.AND
                    )
                case _:
                    raise Exception("Неизвестный фильтр")

        return filter_condition

    def create(self, *args, **object_data: dict[str, Any]) -> Operation:
        """Создание объекта"""
        raw_category = object_data.get("category")
        if raw_category is not None and isinstance(raw_category, int):
            object_data.pop("category")
            object_data["category_id"] = raw_category

        return super().create(*args, **object_data)  # type: ignore
