import datetime
from typing import Any

import pytest

from server.app.operations.enums import OperationTypeEnum
from server.app.operations.models import Operation
from server.app.operations.services import OperationService
from tests.factories.goals import CategoryFactory
from tests.factories.operations import OperationFactory
from tests.factories.user import UserFactory


class TestOperationService:
    """Проверка основных методов сервиса"""

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "create_params",
        [
            # Часть параметров дб указано
            pytest.param(
                {
                    "name": None,
                    "description": None,
                    "operation_at": None,
                    "operation_type": None,
                    "cost": None,
                    "category": None,
                },
                marks=pytest.mark.xfail,
            ),
            # Проверка создания операции Пополнения
            pytest.param(
                {
                    "name": "Пополнение",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 1,
                }
            ),
            # Проверка создания операции Списания
            pytest.param(
                {
                    "name": "Списание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 1,
                }
            ),
            # Проверка создания операции Пополнения с заполненными данными
            pytest.param(
                {
                    "name": "Пополнение",
                    "description": "Описание",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 1,
                    "category": 1,
                }
            ),
            # Проверка создания операции Списания с заполненными данными
            pytest.param(
                {
                    "name": "Списание",
                    "description": "Описание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 1,
                    "category": 1,
                }
            ),
            # Проверка создания операции Пополнения с заполненными данными кроме категории
            pytest.param(
                {
                    "name": "Пополнение",
                    "description": "Описание",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 1,
                    "category": None,
                }
            ),
            # Проверка создания операции Списания с заполненными данными кроме категории
            pytest.param(
                {
                    "name": "Списание",
                    "description": "Описание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 1,
                    "category": None,
                }
            ),
        ]
    )
    def test_create(
        self,
        create_params: dict[str, Any]
    ):
        """Тест проверки создания операции пользователя"""
        user = UserFactory.create()
        _ = CategoryFactory.create()

        service = OperationService(user)
        result = service.create(**create_params)

        # Проверка создания записи
        assert Operation.objects.count() == 1

        # Проверка атрибутов
        for each_create_param_name, each_create_param_value in create_params.items():
            current_value = (
                getattr(result, each_create_param_name) if each_create_param_name != "category"
                else getattr(result, "category_id")
            )

            assert current_value == each_create_param_value

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "user_id, expected",
        [
            (1, 1),
            (None, 0),
        ]
    )
    def test_retrieve_list_filter_by_user(self, user_id: int | None, expected: int):
        """Тест проверки фильтрации данных по пользователю"""
        user = UserFactory.create()
        _ = (
            OperationFactory.create(user=user) if user_id
            else OperationFactory.create()
        )

        service = OperationService(user=user)
        operations = service.retrieve_list()

        assert operations.count() == expected
