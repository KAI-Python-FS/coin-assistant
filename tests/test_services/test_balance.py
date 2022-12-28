
import pytest

from typing import Any

from server.app.operations.dataclasses import (
    BalanceDetailedByCategories,
    BalanceDetailedByCategoriesCategoryItem,
)
from server.app.operations.enums import OperationTypeEnum
from server.app.operations.models import Category
from server.app.operations.services import BalanceService

from tests.factories.category import CategoryFactory
from tests.factories.operations import OperationFactory
from tests.factories.user import UserFactory


class TestBalanceService:
    """Тесты проверки работы сервиса Баланса пользователя"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "user1_spending_operation_values, user1_refill_operation_values, "
        "user2_spending_operation_values, user2_refill_operation_values, user1_expected",
        [
            pytest.param(
                [], [], [], [], 0, id="no_users_operations",
            ),
            pytest.param(
                [1, 2], [], [], [], -3, id="user1_only_spending",
            ),
            pytest.param(
                [], [1, 2], [], [], 3, id="user1_only_refill",
            ),
            pytest.param(
                [], [], [1, 2], [], 0, id="user1_no_operations_user2_only_spending",
            ),
            pytest.param(
                [], [], [], [1, 2], 0, id="user1_no_operations_user2_only_refill",
            ),
            pytest.param(
                [1, 2], [3, 4], [], [], 4, id="user1_all_operations_user2_no_operations",
            ),
            pytest.param(
                [1, 2], [3, 4], [5, 6], [], 4, id="user1_all_operations_user2_only_spending",
            ),
            pytest.param(
                [1, 2], [3, 4], [], [7, 9], 4, id="user1_all_operations_user2_only_refill",
            ),
            pytest.param(
                [1, 2], [3, 4], [5, 6], [7, 9], 4, id="user1_all_operations_user2_all_operations",
            ),
        ]
    )
    def test_retrieve_current_balance_with_few_users(
        self,
        user1_spending_operation_values: list[float],
        user1_refill_operation_values: list[float],
        user1_expected: float,
        user2_spending_operation_values: list[float],
        user2_refill_operation_values: list[float],
    ):
        """Тест текущего баланса с учетом нескольких пользователей"""
        user1, user2 = UserFactory.create_batch(2)
        for each_value in user1_spending_operation_values:
            OperationFactory.create(
                user=user1,
                cost=each_value,
                operation_type=OperationTypeEnum.SPENDING,
            )
        for each_value in user1_refill_operation_values:
            OperationFactory.create(
                user=user1,
                cost=each_value,
                operation_type=OperationTypeEnum.REFILL,
            )
        for each_value in user2_spending_operation_values:
            OperationFactory.create(
                user=user2,
                cost=each_value,
                operation_type=OperationTypeEnum.SPENDING,
            )
        for each_value in user2_refill_operation_values:
            OperationFactory.create(
                user=user2,
                cost=each_value,
                operation_type=OperationTypeEnum.REFILL,
            )

        service = BalanceService(user=user1)
        result = service.retrieve_current_balance()

        assert result == user1_expected

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "spending_operation_params, refill_operation_params, expected",
        [
            pytest.param(
                [], [], BalanceDetailedByCategories(spending=[], refill=[], balance=0),
                id="no_user_operations"
            ),
            pytest.param(
                [
                    {
                        "value": 1,
                    },
                    {
                        "value": 1,
                        "category": 1,
                        "category_name": "Категория 1",
                    },
                    {
                        "value": 2,
                        "category": 1,
                        "category_name": "Категория 1",
                    },
                    {
                        "value": 4,
                        "category": 2,
                        "category_name": "Категория 2",
                    },
                ],
                [],
                BalanceDetailedByCategories(
                    spending=[
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=None,
                            category_name=None,
                            total=1.0,
                        ),
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=1,
                            category_name="Категория 1",
                            total=3.0,
                        ),
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=2,
                            category_name="Категория 2",
                            total=4.0,
                        ),
                    ],
                    refill=[],
                    balance=-8.0,
                ),
                id="only_spending_operations",
            ),
            pytest.param(
                [],
                [
                    {
                        "value": 1,
                    },
                    {
                        "value": 2,
                        "category": 1,
                        "category_name": "Категория 1",
                    },
                    {
                        "value": 3,
                        "category": 2,
                        "category_name": "Категория 2",
                    },
                    {
                        "value": 4,
                        "category": 2,
                        "category_name": "Категория 2",
                    },
                ],
                BalanceDetailedByCategories(
                    spending=[],
                    refill=[
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=None,
                            category_name=None,
                            total=1.0,
                        ),
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=1,
                            category_name="Категория 1",
                            total=2.0,
                        ),
                        BalanceDetailedByCategoriesCategoryItem(
                            category_id=2,
                            category_name="Категория 2",
                            total=7.0,
                        ),
                    ],
                    balance=10.0,
                ),
                id="only_refill_operations",
            ),
        ],
    )
    def test_retrieve_current_balance_detailed(
        self,
        spending_operation_params: list[dict[str, Any]],
        refill_operation_params: list[dict[str, Any]],
        expected: BalanceDetailedByCategories,
    ):
        """Тест детализации текущего баланса"""
        user = UserFactory.create()
        for each_idx in range(1, 5):
            CategoryFactory.create(
                name=f"Категория {each_idx}"
            )
        for each_refill_operation_value in spending_operation_params:
            category_id = (
                each_refill_operation_value.get("category")
            )
            OperationFactory.create(
                cost=each_refill_operation_value["value"],
                category=(
                    Category.objects.get(pk=category_id) if category_id
                    else None
                ),
                user=user,
                operation_type=OperationTypeEnum.SPENDING,
            )
        for each_refill_operation_value in refill_operation_params:
            category_id = (
                each_refill_operation_value.get("category")
            )
            OperationFactory.create(
                cost=each_refill_operation_value["value"],
                category=(
                    Category.objects.get(pk=category_id) if category_id
                    else None
                ),
                operation_type=OperationTypeEnum.REFILL,
                user=user,
            )

        service = BalanceService(user=user)
        result = service.retrieve_current_balance_detailed()

        assert result == expected
