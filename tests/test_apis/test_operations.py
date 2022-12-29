
import json

import pytest

from tests.factories.category import CategoryFactory
from tests.factories.operations import OperationFactory


class TestOperationEndpoints:
    """Тест эндпоинта операций пользователя"""

    endpoint = "/operation/"

    @pytest.mark.django_db()
    def test_list(self, api_client_authorized, api_user):
        """Проверка получения списка операций пользователя"""
        OperationFactory.create_batch(3, user=api_user)

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
                    "operation_type": "Трата",
                    "cost": 2,
                },
            ),
            pytest.param(
                {
                    "name": "тестовое имя",
                    "operation_type": "Пополнение",
                    "cost": 3,
                },
            ),
        ]
    )
    def test_create(self, api_client_authorized, create_params: dict):
        """Проверка создания Операции"""
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
        response_as_json = json.loads(response.content)
        # Проверка наличия переданных значений в ответе
        for each_create_param_name, each_create_param_value in expected.items():
            assert response_as_json[each_create_param_name] == each_create_param_value
