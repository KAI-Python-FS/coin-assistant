
import json

import pytest

from server.app.operations.enums import OperationTypeEnum
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
        # Проверка наличия переданных значений в ответе
        response_as_json = json.loads(response.content)
        for each_create_param_name, each_create_param_value in expected.items():
            assert response_as_json[each_create_param_name] == each_create_param_value

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
            {
                "operation_type": OperationTypeEnum.REFILL,
            },
            {
                "operation_type": OperationTypeEnum.SPENDING,
            },
            {
                "operation_type": OperationTypeEnum.REFILL,
                "category": None,
            },
            {
                "operation_type": OperationTypeEnum.SPENDING,
                "category": None,
            },
        ]
    )
    def test_retrieve_single(self, api_client_authorized, api_user, create_params):
        """Проверка получения Операции"""
        operation = OperationFactory.create(
            user=api_user,
            **create_params,
        )
        url = f'{self.endpoint}{operation.id}'
        expected = {
            "id": operation.id,
            "name": operation.name,
            "description": operation.description,
            "operation_type": operation.operation_type,
            "cost": operation.cost,
            "operation_at": operation.operation_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "category": {
                "id": operation.category.id,
                "name": operation.category.name,
            } if operation.category else None,
        }

        response = api_client_authorized.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "update_params",
        [
            {
                "name": "Новое название операции",
            },
            {
                "category": None,
            },
        ]
    )
    def test_update(self, api_client_authorized, api_user, update_params):
        """Проверка обновления Операции"""
        operation = OperationFactory.create(
            user=api_user,
        )
        url = f'{self.endpoint}{operation.id}'
        expected = {
            "id": operation.id,
            "name": update_params.get("name") or operation.name,
            "description": operation.description,
            "operation_type": operation.operation_type,
            "cost": operation.cost,
            "operation_at": operation.operation_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "category": ({
                    "id": operation.category.id,
                    "name": operation.category.name,
                } if "category" not in update_params.keys()
                else None
            ),
        }

        response = api_client_authorized.put(
            url,
            data=update_params,
            format="json",
        )

        assert response.status_code == 200
        assert json.loads(response.content) == expected
