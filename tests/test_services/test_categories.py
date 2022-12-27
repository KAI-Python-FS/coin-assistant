
from typing import Any

import pytest

from server.app.operations.models import Category
from server.app.operations.services import CategoryService
from tests.factories.category import CategoryFactory


class TestCategoryService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "create_params",
        [
            pytest.param(
                {
                    "name": None,
                },
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                {
                    "name": "Категория123",
                },
            ),
        ]
    )
    def test_create(
        self,
        create_params: dict[str, Any],
    ):
        """Тест проверки создания категории"""
        service = CategoryService()
        _ = service.create(**create_params)

        assert Category.objects.count() == 1

    @pytest.mark.django_db()
    def test_retrieve_list(self):
        """Тест проверки получения данных категорий"""
        _ = CategoryFactory.create_batch(3)

        service = CategoryService()

        assert service.retrieve_list().count() == 3
