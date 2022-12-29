
import json

import pytest

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
