import datetime
import json

import pytest

from server.app.goals.enums import GoalStateEnum, GoalTypeEnum, GoalRefillRuleEnum
from tests.utils import get_formatted_datetime
from tests.factories.category import CategoryFactory
from tests.factories.goals import GoalRefillFactory


class TestGoalRefillEndpoints:
    """Тест эндпоинта целей накопления пользователя"""

    endpoint = "/goal/"

    @pytest.mark.django_db()
    def test_list(self, api_client_authorized, api_user):
        """Проверка получения списка целей накопления пользователя"""
        GoalRefillFactory.create_batch(3, user=api_user)

        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param(
                {
                    "name": "тестовое имя",
                    "value": 2,
                    "state": GoalStateEnum.unknown,
                    "rule": GoalRefillRuleEnum.eq,
                },
            ),
        ]
    )
    def test_create(self, api_client_authorized, create_params: dict):
        """Проверка создания цели накопления"""
        expected = {
            "id": 1,
            **create_params,
        }

        response = api_client_authorized.post(
            self.endpoint,
            data=create_params,
            format="json",
        )

        assert response.status_code == 201
        # Проверка наличия переданных значений в ответе
        response_as_json = json.loads(response.content)
        for each_create_param_name, each_create_param_value in expected.items():
            assert response_as_json[each_create_param_name] == each_create_param_value
