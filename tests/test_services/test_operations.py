import datetime
from typing import Any

import pytest

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

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
        ],
    )
    def test_create(self, create_params: dict[str, Any]):
        """Тест проверки создания операции пользователя"""
        user = UserFactory.create()
        _ = CategoryFactory.create()

        service = OperationService(user)
        result = service.create(**create_params)

        # Проверка создания записи
        assert isinstance(result, Operation)
        assert Operation.objects.count() == 1

        # Проверка атрибутов
        for each_create_param_name, each_create_param_value in create_params.items():
            current_value = (
                getattr(result, each_create_param_name)
                if each_create_param_name != "category"
                else getattr(result, "category_id")
            )

            assert current_value == each_create_param_value

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "create_params",
        [
            # Проверка создания операции Списания со значением 0
            pytest.param(
                {
                    "name": "Списание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 0,
                },
            ),
            # Проверка создания операции Списания со значением -1
            pytest.param(
                {
                    "name": "Списание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": -1,
                },
            ),
            # Проверка создания операции Пополнения со значением 0
            pytest.param(
                {
                    "name": "Пополнение",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 0,
                },
            ),
            # Проверка создания операции Пополнения со значением -1
            pytest.param(
                {
                    "name": "Пополнение",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": -1,
                },
            ),
        ],
    )
    def test_create_with_validation_error(
        self,
        create_params: dict[str, Any],
    ):
        """Тест проверки наличия ошибок валидации при создании операции пользователя"""
        user = UserFactory.create()
        _ = CategoryFactory.create()

        service = OperationService(user)
        with pytest.raises(ValidationError):
            service.create(**create_params)

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "user_id, expected",
        [
            (1, 1),
            (None, 0),
        ],
    )
    def test_retrieve_list_filter_by_user(self, user_id: int | None, expected: int):
        """Тест проверки фильтрации данных по пользователю"""
        user = UserFactory.create()
        _ = OperationFactory.create(user=user) if user_id else OperationFactory.create()

        service = OperationService(user=user)
        operations = service.retrieve_list()

        assert isinstance(operations, QuerySet)
        assert operations.count() == expected

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "filter_params, expected",
        [
            pytest.param(
                {"by_categories": (1,)},
                2,
                id="filter_by_category",
            ),
            pytest.param(
                {"by_operation_type": OperationTypeEnum.REFILL},
                2,
                id="filter_by_operation_type_refill",
            ),
            pytest.param(
                {"by_operation_type": OperationTypeEnum.SPENDING},
                3,
                id="filter_by_operation_type_spending",
            ),
            pytest.param(
                {
                    "by_operation_start_date": datetime.date.today()
                    + datetime.timedelta(days=360),
                },
                0,
                id="filter_by_operation_start_date_next_date",
            ),
            pytest.param(
                {
                    "by_operation_start_date": datetime.date.today()
                    - datetime.timedelta(days=10),
                },
                5,
                id="filter_by_operation_start_date_current_date",
            ),
            pytest.param(
                {
                    "by_operation_finish_date": datetime.date.today()
                    + datetime.timedelta(days=360),
                },
                5,
                id="filter_by_operation_finish_date_current_date",
            ),
            pytest.param(
                {
                    "by_operation_finish_date": datetime.date.today()
                    + datetime.timedelta(days=3),
                },
                2,
                id="filter_by_operation_finish_date_next_date",
            ),
        ],
    )
    def test_retrieve_list_filter(self, filter_params: dict[str, Any], expected: int):
        """Тест проверки данных по передаваемым параметрам"""
        user, category = UserFactory.create(), CategoryFactory.create()
        _ = OperationFactory.create_batch(
            2,
            user=user,
            name="Операция",
            description="Описание",
            operation_type=OperationTypeEnum.REFILL,
            operation_at=datetime.datetime.now() + datetime.timedelta(days=2),
            cost=1,
            category=category,
        )
        _ = OperationFactory.create_batch(
            3,
            user=user,
            name="Операция",
            description="Описание",
            operation_type=OperationTypeEnum.SPENDING,
            operation_at=datetime.datetime.now() + datetime.timedelta(days=10),
            cost=3,
        )

        service = OperationService(user=user)
        operations = service.retrieve_list(**filter_params)

        assert isinstance(operations, QuerySet)
        assert operations.count() == expected

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "operation_id, expected",
        [
            pytest.param(1, 1, id="operation_user"),
            pytest.param(4, None, id="operation_user_another_user"),
        ],
    )
    def test_retrieve_single(self, operation_id: int, expected: int | None):
        """Тест проверки получения единственной записи"""
        user = UserFactory.create()
        _ = [
            OperationFactory.create(user=user),
            OperationFactory.create(),
        ]

        service = OperationService(user=user)
        result = service.retrieve_single(operation_id)

        assert isinstance(result, Operation) if result else result is None
        assert result.id == expected if result is not None else result is None

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "update_params",
        [
            pytest.param(
                {
                    "name": "Новое название",
                    "description": "Новое описание",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 4,
                },
                id="update_operation_refill_most_params",
            ),
            pytest.param(
                {
                    "name": "Новое название",
                    "description": "Новое описание",
                    "operation_type": OperationTypeEnum.REFILL,
                    "cost": 4,
                    "category": 1,
                },
                id="update_operation_refill_category",
            ),
            pytest.param(
                {
                    "name": "Новое название",
                    "description": "Новое описание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 4,
                },
                id="update_operation_spending_most_params",
            ),
            pytest.param(
                {
                    "name": "Новое название",
                    "description": "Новое описание",
                    "operation_type": OperationTypeEnum.SPENDING,
                    "cost": 4,
                    "category": 1,
                },
                id="update_operation_spending_category",
            ),
        ],
    )
    def test_update(
        self,
        update_params: dict,
    ):
        """Тест проверки обновления данных"""
        user = UserFactory()
        CategoryFactory.create()
        existing_operation = OperationFactory(
            user=user,
        )

        service = OperationService(user=user)
        result = service.update(existing_operation.id, **update_params)

        assert isinstance(result, Operation)
        for each_update_param_key, each_update_param_value in update_params.items():
            if each_update_param_key == "category":
                assert getattr(result, "category_id") == each_update_param_value
            else:
                assert getattr(result, each_update_param_key) == each_update_param_value

    @pytest.mark.django_db(reset_sequences=True)
    @pytest.mark.parametrize(
        "update_params",
        [
            pytest.param(
                {
                    "cost": 0,
                },
                id="cost_equal_to_zero",
            ),
            pytest.param(
                {
                    "cost": -1,
                },
                id="cost_lt_zero",
            ),
            pytest.param(
                {
                    "cost": 0,
                    "operation_type": OperationTypeEnum.REFILL,
                },
                id="cost_equal_to_zero_operation_type_refill",
            ),
            pytest.param(
                {
                    "cost": 0,
                    "operation_type": OperationTypeEnum.SPENDING,
                },
                id="cost_equal_to_zero_operation_type_spending",
            ),
            pytest.param(
                {
                    "cost": -1,
                    "operation_type": OperationTypeEnum.REFILL,
                },
                id="cost_lt_zero_operation_type_refill",
            ),
            pytest.param(
                {
                    "cost": -1,
                    "operation_type": OperationTypeEnum.SPENDING,
                },
                id="cost_lt_zero_operation_type_spending",
            ),
        ],
    )
    def test_update_with_validation_error(self, update_params: dict[str, Any]):
        """Тест проверки обновления данных с возникающей ошибкой валидации"""
        user = UserFactory()
        CategoryFactory.create()
        existing_operation = OperationFactory(
            user=user,
        )

        service = OperationService(user=user)
        with pytest.raises(ValidationError):
            service.update(existing_operation.id, **update_params)

    @pytest.mark.django_db()
    def test_delete(self):
        """Тест проверки удаления записи"""
        existing_operation = OperationFactory.create()

        service = OperationService(
            user=existing_operation.user,
        )
        result = service.delete(existing_operation.id)

        assert isinstance(result, bool)
        assert Operation.objects.count() == 0

    @pytest.mark.django_db()
    def test_delete_non_exist(self):
        """Тест проверки удаления записи"""
        user = UserFactory.create()
        existing_operation = OperationFactory.create()

        service = OperationService(user=user)
        result = service.delete(existing_operation.id + 1)

        assert result is None
