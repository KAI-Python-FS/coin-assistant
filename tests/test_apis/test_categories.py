
import json

import pytest

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


