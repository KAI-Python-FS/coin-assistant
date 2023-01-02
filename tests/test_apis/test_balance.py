import datetime
import json

import pytest

from server.app.operations.enums import OperationTypeEnum
from tests.factories.operations import OperationFactory


class TestBalanceEndpoints:
    """Тест эндпоинта текущего баланса пользователя"""

    endpoint = "/balance/"

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
        expected = round(
            sum(
                each_existing_budget.cost
                for each_existing_budget in existing_operations_refill
            ) - sum(
                each_existing_goal_refill.cost
                for each_existing_goal_refill in existing_operations_spending
            ),
            2,
        )

        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert json.loads(response.content) == expected
