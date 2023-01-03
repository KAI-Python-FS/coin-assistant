from typing import Any

from django.db.models import F, Sum, Q

from server.app.base.services import BaseModelCRUDService, BaseModelUserFilterCRUDService

from .enums import OperationTypeEnum
from .models import Category, Operation
from .dataclasses import BalanceDetailedByCategories, BalanceDetailedByCategoriesCategoryItem


class CategoryService(BaseModelCRUDService):
    """Класс описания бизнес логики работы с Категориями покупок"""

    model = Category


class OperationService(BaseModelUserFilterCRUDService):
    """Класс описания бизнес логики работы с Операциями пользователя"""

    model = Operation

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает условия фильтрации получения списка"""
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
                        (
                            Q(category_id__in=each_filter_value)
                            if each_filter_value
                            else Q(category__isnull=True)
                        ),
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

    def create(self, **object_data: dict[str, Any]) -> Operation:
        """Создание объекта"""
        raw_category = object_data.get("category")
        if raw_category is not None and isinstance(raw_category, int):
            object_data.pop("category")
            object_data["category_id"] = raw_category

        return super().create(**object_data)  # type: ignore


class BalanceService:
    """
    Класс описания бизнес логики работы с Балансом пользователя.

    Баланс - это сумма всех операций пополнения минус сумма всех операций списания
    """

    def __init__(self, user):
        super().__init__()

        self.user = user

    def retrieve_current_balance(self) -> float:
        """Получение текущего баланса текущего пользователя"""
        balance_qs = Operation.objects.filter(
            user=self.user
        ).aggregate(
            refill=Sum(
                "cost",
                filter=Q(operation_type=OperationTypeEnum.REFILL.value)
            ),
            spending=Sum(
                "cost",
                filter=Q(operation_type=OperationTypeEnum.SPENDING.value)
            )
        )

        balance = (balance_qs["refill"] or 0) - (balance_qs["spending"] or 0)
        return round(balance, 2)

    def retrieve_current_balance_detailed(self) -> BalanceDetailedByCategories:
        """Получение детализированного представления текущего баланса текущего пользователя"""
        # TODO вот бы это реализовать используя asyncio
        current_balance = self.retrieve_current_balance()

        categories_qs = (
            Operation.objects.filter(
                user=self.user
            ).values(
                "category__pk",
                "category__name",
            ).annotate(
                refill=Sum(
                    "cost",
                    filter=Q(operation_type=OperationTypeEnum.REFILL.value),
                ),
                spending=Sum(
                    "cost",
                    filter=Q(operation_type=OperationTypeEnum.SPENDING.value),
                ),
            ).order_by(
                F("category__pk").asc(nulls_first=True)
            ).all()
        )

        detailed_info: list[dict[str, Any]] = list(categories_qs)

        result = BalanceDetailedByCategories(
            balance=current_balance,
            spending=[
                BalanceDetailedByCategoriesCategoryItem(
                    category_id=each_detailed_info["category__pk"],
                    category_name=each_detailed_info["category__name"],
                    total=each_detailed_info["spending"],
                )
                for each_detailed_info in detailed_info
                if each_detailed_info["spending"] is not None
            ],
            refill=[
                BalanceDetailedByCategoriesCategoryItem(
                    category_id=each_detailed_info["category__pk"],
                    category_name=each_detailed_info["category__name"],
                    total=each_detailed_info["refill"],
                )
                for each_detailed_info in detailed_info
                if each_detailed_info["refill"] is not None
            ]
        )

        return result
