
from server.app.base.exceptions import ValidationException

from .enums import OperationTypeEnum
from .models import Category, Operation


class CategoryService:
    """Класс описания бизнес логики работы с Категориями покупок"""

    @classmethod
    def create(cls, **category_data) -> Category:
        """Создание категории"""
        category = Category.objects.create(**category_data)
        return category

    @classmethod
    def retrieve_single(cls, category_id: int) -> Category | None:
        """Получение одной категории"""
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None

        return category

    @classmethod
    def update(cls, category_id: int, **category_data) -> Category | None:
        """Обновление категории"""
        category = cls.retrieve_single(category_id)
        if not category:
            return None

        category.name = category_data.pop("name")
        category.save()

        return category

    @classmethod
    def delete(cls, category_id: int) -> bool | None:
        """Удаление категории"""
        category = cls.retrieve_single(category_id)
        if not category:
            return None

        category.delete()

        return True

    @classmethod
    def retrieve_list(cls, **filters) -> list[Category | None]:
        """Получение списка категорий согласно фильтрам"""
        return Category.objects.filter(**filters).all()


class OperationService:
    """Класс описания бизнес логики работы с операциями пользователя"""

    def __init__(self, user) -> None:
        self.user = user

    @classmethod
    def create_operation(cls, user, **operation_data) -> Operation:
        """Создание записи операции пользователя"""
        operation = Operation.objects.create(
            user=user,
            **operation_data,
        )

        return operation

    @classmethod
    def retrieve_list(cls, **filters) -> list[Operation | None]:
        return Operation.objects.filter(**filters).all()


    # @classmethod
    # def create_spending(cls, user: int, **operation_data):
    #     """Создание записи траты у пользователя"""
    #     Operation.objects.create(
    #         user=user,
    #         operation_type=OperationTypeEnum.SPENDING,
    #         **operation_data
    #     )
    #
    # @classmethod
    # def create_refill(cls, user: int, **operation_data):
    #     """Создание записи пополнения у пользователя"""
    #     Operation.objects.create(
    #         user=user,
    #         operation_type=OperationTypeEnum.REFILL,
    #         **operation_data
    #     )
