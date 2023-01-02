import datetime
import json

import pytest

from server.app.goals.enums import BudgetRuleEnum, GoalStateEnum
from tests.factories.goals import BudgetFactory
from tests.utils import get_formatted_date


class TestBudgetEndpoints:
    """Тест эндпоинта Бюджета пользователя"""

    endpoint = "/budget/"

    @pytest.mark.django_db()
    def test_list(self, api_client_authorized, api_user):
        """Проверка получения списка Бюджетов пользователя"""
        BudgetFactory.create_batch(3, user=api_user)

        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param(
                {
                    "name": "тестовое имя",
                    "value": 2,
                    "state": GoalStateEnum.unknown,
                    "rule": BudgetRuleEnum.eq,
                },
            ),
        ]
    )
    def test_create(self, api_client_authorized, create_params: dict):
        """Проверка создания Бюджета"""
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

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param({}),
            pytest.param(
                {
                    "finish_date": datetime.datetime.now(),
                },
            ),
        ]
    )
    def test_retrieve_single(self, api_client_authorized, api_user, create_params: dict):
        """Проверка получения Бюджета пользователя"""
        goal_refill = BudgetFactory.create(
            user=api_user,
            **create_params,
        )
        url = f'{self.endpoint}{goal_refill.id}'
        expected = {
            "id": goal_refill.id,
            "name": goal_refill.name,
            "description": goal_refill.description,
            "category": ({
                     "id": goal_refill.category.id,
                     "name": goal_refill.category.name,
                 } if goal_refill.category
                 else None
             ),
            "start_date": get_formatted_date(goal_refill.start_date),
            "finish_date": (
                get_formatted_date(goal_refill.finish_date) if goal_refill.finish_date
                else None
            ),
            "state": goal_refill.state,
            "value": goal_refill.value,
            "rule": goal_refill.rule,
        }

        response = api_client_authorized.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "update_params",
        [
            {
                "name": "Новое название бюджета",
            },
            {
                "category": None,
            },
            {
                "value": 45,
            },
            {
                "rule": BudgetRuleEnum.lte,
            }
        ]
    )
    def test_update(self, api_client_authorized, api_user, update_params):
        """Проверка обновления Бюджета пользователя"""
        budget = BudgetFactory.create(
            user=api_user,
            **update_params,
        )
        url = f'{self.endpoint}{budget.id}'
        expected = {
            "id": budget.id,
            "name": budget.name,
            "description": budget.description,
            "category": ({
                             "id": budget.category.id,
                             "name": budget.category.name,
                         } if budget.category
                         else None
                         ),
            "start_date": get_formatted_date(budget.start_date),
            "finish_date": (
                get_formatted_date(budget.finish_date) if budget.finish_date
                else None
            ),
            "state": budget.state,
            "value": budget.value,
            "rule": budget.rule,
        }

        response = api_client_authorized.put(
            url,
            data=update_params,
            format="json",
        )

        assert response.status_code == 200
        assert json.loads(response.content) == expected

    @pytest.mark.django_db()
    def test_delete(self, api_client_authorized, api_user):
        """Проверка удаления бюджета пользователя"""
        goal_refill = BudgetFactory.create(
            user=api_user,
        )
        url = f'{self.endpoint}{goal_refill.id}'

        response = api_client_authorized.delete(url)

        assert json.loads(response.content) == True
