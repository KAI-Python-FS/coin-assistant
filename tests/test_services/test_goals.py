import datetime
from typing import Any

import pytest
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from server.app.goals.enums import (
    GoalRefillRuleEnum,
    GoalStateEnum,
    GoalTypeEnum,
)
from server.app.goals.models import Goal
from server.app.goals.services import GoalRefillService
from tests.factories.category import CategoryFactory
from tests.factories.goals import GoalRefillFactory
from tests.factories.user import UserFactory


class TestGoalRefillService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params, expected",
        [
            # Проверка заполнения минимальным числом параметров
            pytest.param(
                {
                    "name": "Тест",
                    "value": 1,
                },
                1,
                id="minimal_params",
            ),
        ],
    )
    def test_create(
        self,
        create_params: dict[str, Any],
        expected,
    ):
        """Тест проверки создания цели накопления с различным числом параметров"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        result = service.create(
            object_data=create_params,
        )

        assert isinstance(result, Goal)
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
        ],
    )
    def test_create_default_type(
        self,
        create_params: dict[str, Any],
    ):
        """Тест проверки цели накопления с определенным типом"""
        user = UserFactory()

        service = GoalRefillService(user=user)
        result = service.create(
            object_data=create_params,
        )

        assert isinstance(result, Goal)
        assert result.goal_type == GoalTypeEnum.REFILL

    @pytest.mark.django_db()
    def test_retrieve_list_filter_by_user(self):
        """Тест проверки фильтрации данных по пользователю"""
        goals_refills = GoalRefillFactory.create_batch(
            2,
        )

        for each_goal in goals_refills:
            service = GoalRefillService(user=each_goal.user)
            result = service.retrieve_list()

            assert isinstance(result, QuerySet)  # type: ignore
            assert result.count() == 1

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "filter_params, expected",
        [
            ({"by_categories": (1,)}, 2),
            (
                {
                    "by_state": GoalStateEnum.working,
                },
                2,
            ),
            (
                {
                    "by_start_date": datetime.date.today()
                    + datetime.timedelta(days=360),
                },
                0,
            ),
            (
                {
                    "by_start_date": datetime.date.today()
                    - datetime.timedelta(days=10),
                },
                5,
            ),
            (
                {
                    "by_finish_date": datetime.date.today()
                    + datetime.timedelta(days=360),
                },
                5,
            ),
            (
                {
                    "by_finish_date": datetime.date.today()
                    + datetime.timedelta(days=3),
                },
                2,
            ),
            (
                {
                    "by_budget_rule": GoalRefillRuleEnum.eq,
                },
                2,
            ),
            (
                {
                    "by_budget_rule": GoalRefillRuleEnum.gt,
                },
                3,
            ),
        ],
    )
    def test_retrieve_list_filter(self, filter_params, expected):
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
        result = service.retrieve_list(**filter_params)

        assert result.count() == expected

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "goal_id, expected",
        [
            pytest.param(1, 1, id="users_goal_refill"),
            pytest.param(4, None, id="another_user_goal_refill"),
        ],
    )
    def test_retrieve_single(self, goal_id: int, expected: int | None):
        """Тест проверки получения единственной записи"""
        user = UserFactory()
        _ = [
            GoalRefillFactory(
                user=user,
            ),
            GoalRefillFactory(),
        ]

        service = GoalRefillService(user=user)
        result = service.retrieve_single(goal_id)

        assert (
            isinstance(result, Goal) if result is not None else result is None
        )
        assert result.pk == expected if result is not None else result is None

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "update_params",
        [
            {
                "name": "тест321",
                "description": "интересное описание",
                "category": 1,
                "start_date": datetime.date.today(),
                "finish_date": datetime.date.today()
                + datetime.timedelta(days=3),
                "value": 3,
                "state": GoalStateEnum.succeed,
                "rule": GoalRefillRuleEnum.gte,
            },
            {
                "category": None,
            },
        ],
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

        assert isinstance(result, Goal)
        for (
            each_update_param_key,
            each_update_param_value,
        ) in update_params.items():
            if each_update_param_key == "category":
                assert (
                    getattr(result, "category_id") == each_update_param_value
                )
            else:
                assert (
                    getattr(result, each_update_param_key)
                    == each_update_param_value
                )

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "update_params",
        [
            pytest.param(
                {
                    "goal_type": GoalTypeEnum.REFILL,
                },
                id="existing_field",
            ),
            pytest.param(
                {
                    "field1": 1,
                },
                id="non_existing_field",
            ),
        ],
    )
    def test_update_with_validation_error_on_non_existing_fields(
        self, update_params: dict[str, Any]
    ):
        """Тест проверки возникновения ошибки валидации при передаче полей, недоступных к обновлению"""
        user = UserFactory()
        CategoryFactory.create()
        existing_goal = GoalRefillFactory(
            user=user,
            state=GoalStateEnum.unknown,
            rule=GoalRefillRuleEnum.eq,
        )

        service = GoalRefillService(user=user)
        with pytest.raises(ValidationError):
            service.update(existing_goal.id, **update_params)

    @pytest.mark.django_db()
    def test_delete(self):
        """Тест проверки удаления записи"""
        user = UserFactory()
        existing_goal = GoalRefillFactory(
            user=user,
        )

        service = GoalRefillService(user=user)
        result = service.delete(existing_goal.id)

        assert isinstance(result, bool)
        assert Goal.objects.goals().count() == 0
