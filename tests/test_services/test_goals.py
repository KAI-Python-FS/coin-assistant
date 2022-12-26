
import pytest

from server.app.goals.services import GoalRefillService
from server.app.goals.models import Goal
from server.app.goals.enums import GoalRefillRuleEnum
from tests.factories.user import UserFactory


TEST_DATA_SERVICE_CREATE = [
    ("Тест", None, None, None, None, None, 1, GoalRefillRuleEnum.eq, 1),
    pytest.param(
        None, None, None, None, None, None, 1, GoalRefillRuleEnum.eq, 1, marks=pytest.mark.xfail,
    ),
]


class TestGoalRefillService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "name, description, category, start_date, finish_date, state, value, rule, expected",
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
        expected
    ):
        """Тест проверки создания цели накопления"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        _ = service.create(
            name=name,
            description=description,
            category=category,
            # start_date=start_date,
            finish_date=finish_date,
            state=state,
            value=value,
            rule=rule,
        )

        assert Goal.objects.goals().count() == expected
