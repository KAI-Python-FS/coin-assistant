import datetime
from typing import Any

import pytest

from server.app.goals.services import GoalRefillService
from server.app.goals.enums import GoalTypeEnum, GoalStateEnum, GoalRefillRuleEnum
from server.app.goals.models import Goal
from tests.factories.category import CategoryFactory
from tests.factories.goals import GoalRefillFactory
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
        expected,
    ):
        """Тест проверки создания цели накопления с различным числом параметров"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        _ = service.create(
            **create_params,
        )

        assert Goal.objects.goals().count() == expected

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
        """Тест проверки цели накопления с определенным типом"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        result = service.create(
            **create_params,
        )

        assert result.goal_type == GoalTypeEnum.REFILL

    @pytest.mark.django_db()
    def test_retrieve_list_filter_by_user(self):
        """Тест проверки фильтрации данных по пользователю"""
        goals_refills = GoalRefillFactory.create_batch(
            2,
        )

        for each_goal in goals_refills:
            service = GoalRefillService(user=each_goal.user)
            goals = service.retrieve_list()

            assert len(goals) == 1

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "filter_params, expected",
        [
            (
                {
                    "by_categories": (1,)
                },
                2
            ),
            (
                {
                    "by_state": GoalStateEnum.working,
                },
                2
            ),
            (
                {
                    "by_start_date": datetime.date.today() + datetime.timedelta(days=360),
                },
                0,
            ),
            (
                {
                    "by_start_date": datetime.date.today() - datetime.timedelta(days=10),
                },
                5,
            ),
            (
                {
                    "by_finish_date": datetime.date.today() + datetime.timedelta(days=360),
                },
                5,
            ),
            (
                {
                    "by_finish_date": datetime.date.today() + datetime.timedelta(days=3),
                },
                2,
            ),
            (
                {
                    "by_budget_rule": GoalRefillRuleEnum.eq,
                },
                2
            ),
            (
                {
                    "by_budget_rule": GoalRefillRuleEnum.gt,
                },
                3
            ),
        ],
    )
    def test_retrieve_list_filter_p(self, filter_params, expected):
        """Тест проверки фильтрации данных по передаваемым параметрам"""
        user = UserFactory()
        category = CategoryFactory.create()
        _ = GoalRefillFactory.create_batch(
            2,
            user=user,
            category=category,
            state=GoalStateEnum.working,
            start_date=datetime.date.today(),
            finish_date=datetime.date.today() + datetime.timedelta(days=3),
            rule=GoalRefillRuleEnum.eq,
        )
        _ = GoalRefillFactory.create_batch(
            3,
            user=user,
            state=GoalStateEnum.unknown,
            start_date=datetime.date.today() + datetime.timedelta(days=10),
            rule=GoalRefillRuleEnum.gt,
        )

        service = GoalRefillService(user=user)
        goals = service.retrieve_list(**filter_params)

        assert len(goals) == expected

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "update_params",
        [
            {
                "name": "тест321",
                "description": "интересное описание",
                "category": 1,
                "start_date": datetime.date.today(),
                "finish_date": datetime.date.today() + datetime.timedelta(days=3),
                "value": 3,
                "state": GoalStateEnum.succeed,
                "rule": GoalRefillRuleEnum.gte,
            },
            {
                "category": None,
            },
            pytest.param(
                {
                    "goal_type": GoalTypeEnum.SPENDING,
                },
                marks=pytest.mark.xfail,
            ),
        ]
    )
    def test_update(
        self,
        update_params: dict,
    ):
        """Тест проверки обновления данных"""
        user = UserFactory()
        CategoryFactory.create()
        existing_goal = GoalRefillFactory(
            user=user,
            state=GoalStateEnum.unknown,
            rule=GoalRefillRuleEnum.eq,
        )

        service = GoalRefillService(user=user)
        result = service.update(existing_goal.id, **update_params)

        for each_update_param_key, each_update_param_value in update_params.items():
            if each_update_param_key == "category":
                assert getattr(result, "category_id") == each_update_param_value
            else:
                assert getattr(result, each_update_param_key) == each_update_param_value

    @pytest.mark.django_db()
    def test_delete(self):
        """Тест проверки удаления записи"""
        user = UserFactory()
        existing_goal = GoalRefillFactory(
            user=user,
        )

        service = GoalRefillService(user=user)
        service.delete(existing_goal.id)

        assert Goal.objects.goals().count() == 0
