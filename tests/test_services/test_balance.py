
import pytest

from server.app.operations.enums import OperationTypeEnum
from server.app.operations.services import BalanceService

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
