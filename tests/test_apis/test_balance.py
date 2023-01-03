import datetime
import json

import pytest

from server.app.operations.enums import OperationTypeEnum
from server.app.operations.models import Operation
from tests.factories.operations import OperationFactory


class TestBalanceEndpoints:
    """Тест эндпоинта текущего баланса пользователя"""

    endpoint = "/balance/"

    @staticmethod
    def _get_expected_balance(
        operations_refill: list[Operation],
        operations_spending: list[Operation],
    ) -> float:
        """Метод, возвращающий баланс пользователя по переданным операциям пополнения и списания"""
        return round(
            sum(
                each_operation_refill.cost
                for each_operation_refill in operations_refill
            ) - sum(
                each_operation_spending.cost
                for each_operation_spending in operations_spending
            ),
            2,
        ) or 0

    @pytest.mark.django_db()
    def test_balance(self, api_client_authorized, api_user):
        """Проверка получения текущего баланса пользователя"""
        existing_operations_refill = OperationFactory.create_batch(
            2,
            operation_type=OperationTypeEnum.REFILL,
            user=api_user,
        )
        existing_operations_spending = OperationFactory.create_batch(
            2,
            operation_type=OperationTypeEnum.SPENDING,
            user=api_user,
        )
        expected = self._get_expected_balance(
            operations_refill=existing_operations_refill,
            operations_spending=existing_operations_spending,
        )

        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert json.loads(response.content) == expected

    @pytest.mark.django_db()
    def test_empty_balance(self, api_client_authorized, api_user):
        """Проверка получения текущего баланса пользователя при отсутствующих операциях"""
        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert json.loads(response.content) == 0

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param(
                {
                    "operations_refill_len": 0,
                    "operations_spending_len": 0,
                },
            ),
            pytest.param(
                {
                    "operations_refill_len": 1,
                    "operations_spending_len": 0,
                },
            ),
            pytest.param(
                {
                    "operations_refill_len": 0,
                    "operations_spending_len": 1,
                },
            ),
            pytest.param(
                {
                    "operations_refill_len": 1,
                    "operations_spending_len": 1,
                },
            ),
        ]
    )
    def test_balance_detailed(self, api_client_authorized, api_user, create_params: dict):
        """Тест проверки детализированного баланса пользователя"""
        existing_operations_refill = (
            OperationFactory.create_batch(
                create_params["operations_refill_len"],
                operation_type=OperationTypeEnum.REFILL,
                user=api_user,
            ) if create_params["operations_refill_len"]
            else []
        )
        existing_operations_spending = (
            OperationFactory.create_batch(
                create_params["operations_spending_len"],
                operation_type=OperationTypeEnum.SPENDING,
                user=api_user,
            ) if create_params["operations_spending_len"]
            else []
        )
        expected = {
            "balance": self._get_expected_balance(
                operations_refill=existing_operations_refill,
                operations_spending=existing_operations_spending,
            ),
            "spending": [{
                    "category_id": each_operation_spending.category.id,
                    "category_name": each_operation_spending.category.name,
                    "total": round(each_operation_spending.cost, 2),
                }
                for each_operation_spending in existing_operations_spending
            ],
            "refill": [{
                    "category_id": each_operation_refill.category.id,
                    "category_name": each_operation_refill.category.name,
                    "total": round(each_operation_refill.cost, 2),
                }
                for each_operation_refill in existing_operations_refill
            ],
        }
        url = f'{self.endpoint}detailed/'

        response = api_client_authorized.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected
