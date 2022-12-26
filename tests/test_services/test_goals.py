
from typing import Any

import pytest

from server.app.goals.services import GoalRefillService
from server.app.goals.models import Goal
from tests.factories.user import UserFactory


TEST_DATA_SERVICE_CREATE = [
    # Часть параметров дб указано
    pytest.param(
        {
            "name": None,
            "description": None,
            "category": None,
            "start_date": None,
            "finish_date": None,
            "state": None,
            "value": None,
            "rule": None,
        },
        0,
        marks=pytest.mark.xfail,
        id="all_params_none"
    ),
    # Проверка заполнения минимальным числом параметров
    pytest.param(
        {
            "name": "Тест",
            "value": 1,
        },
        1,
        id="minimals_params"
    ),
]


class TestGoalRefillService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params, expected",
        TEST_DATA_SERVICE_CREATE,
    )
    def test_create(
        self,
        create_params: dict[str, Any],
        expected
    ):
        """Тест проверки создания цели накопления с различным числом параметров"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        _ = service.create(
            **create_params,
        )

        assert Goal.objects.goals().count() == expected
