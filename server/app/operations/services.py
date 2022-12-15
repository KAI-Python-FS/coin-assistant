
from .enums import OperationTypeEnum
from .models import Operation


class OperationService:
    """Класс описания бизнес логики работы с операциями пользователя"""

    @classmethod
    def create_operation(cls, user, **operation_data):
        """Создание записи операции пользователя"""

    @classmethod
    def create_spending(cls, user: int, **operation_data):
        """Создание записи траты у пользователя"""
        Operation.objects.create(
            user=user,
            operation_type=OperationTypeEnum.SPENDING,
            **operation_data
        )

    @classmethod
    def create_refill(cls, user: int, **operation_data):
        """Создание записи пополнения у пользователя"""
        Operation.objects.create(
            user=user,
            operation_type=OperationTypeEnum.REFILL,
            **operation_data
        )
