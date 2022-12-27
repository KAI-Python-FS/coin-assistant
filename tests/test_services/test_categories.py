
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

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "category_id, expected",
        [
            pytest.param(1, 1),
            pytest.param(4, None),
        ]
    )
    def test_retrieve_single(self, category_id: int, expected: int | None):
        """Тест проверки получения единственной записи"""
        _ = CategoryFactory.create_batch(3)

        service = CategoryService()
        result = service.retrieve_single(category_id)

        assert (
            result.id == expected if result is not None
            else result is None
        )

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "update_params",
        [
            {
                "name": "тест321"
            },
            pytest.param(
                {
                    "name": None
                },
                marks=pytest.mark.xfail,
            ),
        ]
    )
    def test_update(self, update_params):
        """Тест проверки обновления данных"""
        existing_category = CategoryFactory.create()

        service = CategoryService()
        result = service.update(existing_category.id, **update_params)

        for each_update_param_key, each_update_param_value in update_params.items():
            assert getattr(result, each_update_param_key) == each_update_param_value
