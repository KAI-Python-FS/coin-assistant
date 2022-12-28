
import pytest

from server.app.operations.enums import OperationTypeEnum
from server.app.operations.services import BalanceService

from tests.factories.operations import OperationFactory
from tests.factories.user import UserFactory


class TestBalanceService:
    """Тесты проверки работы сервиса Баланса пользователя"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "spending_operation_values, refill_operation_values, expected",
        [
            pytest.param(
                [], [], 0, id="no_user_operation"
            ),
            pytest.param(
                [1.1, 2.2], [], -3.3, id="user_operation_only_spending",
            ),
            pytest.param(
                [], [1.2, 3.4], 4.6, id="user_operation_only_refill",
            ),
            pytest.param(
                [2, 1.3], [4.4, 1.2], 2.3, id="user_operations_both",
            )
        ]
    )
    def test_retrieve_current_balance(
        self,
        spending_operation_values: list[float],
        refill_operation_values: list[float],
        expected: float,
    ):
        """Тест текущего баланса пользователя"""
        user = UserFactory.create()
        for each_value in spending_operation_values:
            OperationFactory.create(
                user=user,
                cost=each_value,
                operation_type=OperationTypeEnum.SPENDING,
            )
        for each_value in refill_operation_values:
            OperationFactory.create(
                user=user,
                cost=each_value,
                operation_type=OperationTypeEnum.REFILL,
            )

        service = BalanceService(user=user)
        result = service.retrieve_current_balance()

        assert result == expected
