
import json

import pytest

from server.app.operations.serializers import CategoryCreateInputSerializer, CategoryCreateOutputSerializer
from tests.factories.category import CategoryFactory
from tests.factories.user import UserFactory


class TestCategoryEndpoints:
    """Тест эндпоинта категорий"""

    endpoint = "/category/"

    @pytest.mark.django_db()
    def test_list(self, api_client_authorized):
        """Проверка получения списка категорий"""
        CategoryFactory.create_batch(3)

        response = api_client_authorized.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    @pytest.mark.django_db(reset_sequences=True)
    def test_create(self, api_client_authorized):
        """Проверка создания категории"""
        input_params = {
            "name": "Тест",
        }

        response = api_client_authorized.post(
            self.endpoint,
            data=input_params,
            format="json",
        )

        assert response.status_code == 201
        assert json.loads(response.content) == {
            "id": 1,
            "name": input_params["name"],
        }
