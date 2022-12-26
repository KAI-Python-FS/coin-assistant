
import datetime

from typing import Any

import pytest

from server.app.goals.enums import BudgetRuleEnum, GoalTypeEnum, GoalStateEnum
from server.app.goals.services import BudgetService
from server.app.goals.models import Goal
from tests.factories.category import CategoryFactory
from tests.factories.goals import BudgetFactory
from tests.factories.user import UserFactory


class TestBudgetService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
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
                marks=pytest.mark.xfail,
                id="all_params_none"
            ),
            # Проверка заполнения минимальным числом параметров
            pytest.param(
                {
                    "name": "Тест",
                    "value": 1,
                },
                id="minimals_params"
            ),
        ]
    )
    def test_create(
        self,
        create_params: dict[str, Any],
    ):
        """Тест проверки создания бюджета с различным числом параметров"""
        user = UserFactory()

        service = BudgetService(user=user)
        _ = service.create(
            **create_params,
        )

        assert Goal.objects.budgets().count() == 1

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param(
                {
                    "name": "Тест",
                    "value": 1,
                },
                id="no_state",
            ),
            pytest.param(
                {
                    "name": "Тест",
                    "value": 1,
                    "state": GoalTypeEnum.SPENDING,
                },
                id="incorrect_state",
            ),
        ]
    )
    def test_create_default_type(
        self,
        create_params: dict[str, Any],
    ):
        """Тест проверки бюджета с определенным типом"""
        user = UserFactory()

        service = BudgetService(user=user)
        result = service.create(
            **create_params,
        )

        assert result.goal_type == GoalTypeEnum.SPENDING

    @pytest.mark.django_db()
    def test_retrieve_list_filter_by_user(self):
        """Тест проверки фильтрации бюджетов по пользователю"""
        goals_refills = BudgetFactory.create_batch(
            2,
        )

        for each_goal in goals_refills:
            service = BudgetService(user=each_goal.user)
            goals = service.retrieve_list()

            assert len(goals) == 1

