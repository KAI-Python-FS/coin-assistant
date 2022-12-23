
import pytest

from server.app.goals.services import GoalRefillService
from server.app.goals.models import Goal
from server.app.goals.enums import GoalRefillRuleEnum
from tests.factories.user import UserFactory


TEST_DATA_SERVICE_CREATE = [
    ("Тест", None, None, None, None, None, 1, GoalRefillRuleEnum.eq, )
    # pytest.param("6*9", 42, marks=pytest.mark.xfail)
]


class TestGoalRefillService:
    """Проверка основных методов сервиса"""

    @pytest.mark.parametrize(
        "name, description, category, start_date, finish_date, state, value, rule",
        TEST_DATA_SERVICE_CREATE,
    )
    def test_create(
        self,
        name,
        description,
        category,
        start_date,
        finish_date,
        state,
        value,
        rule,
    ):
        """Тест проверки создания цели накопления"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        result = service.create(
            name, description, category, start_date, finish_date, state, value, rule
        )

        assert Goal.objects.
