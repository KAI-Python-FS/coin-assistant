import json

import pytest

from tests.factories.category import CategoryFactory


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

    @pytest.mark.django_db()
    def test_retrieve_single(self, api_client_authorized):
        """Проверка получения единственной категории"""
        category = CategoryFactory.create()
        url = f"{self.endpoint}{category.id}"

        response = api_client_authorized.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == {
            "id": category.id,
            "name": category.name,
        }

    @pytest.mark.django_db()
    def test_update(self, api_client_authorized):
        """Проверка обновления единственной категории"""
        category = CategoryFactory.create()
        url = f"{self.endpoint}{category.id}"
        input_params = {
            "name": "Тест2",
        }

        response = api_client_authorized.put(
            url,
            data=input_params,
            format="json",
        )

        assert response.status_code == 200
        assert json.loads(response.content) == {
            "id": category.id,
            "name": input_params["name"],
        }

    @pytest.mark.django_db()
    def test_delete(self, api_client_authorized):
        """Проверка удаления единственной категории"""
        category = CategoryFactory.create()
        url = f"{self.endpoint}{category.id}"

        response = api_client_authorized.delete(url)

        assert json.loads(response.content)
