
from django.core.exceptions import FieldDoesNotExist

from server.app.base.services import BaseModelCRUDService, BaseModelUserFilterCRUDService

from .models import Category, Operation


class CategoryService(BaseModelCRUDService):
    """Класс описания бизнес логики работы с Категориями покупок"""

    model = Category


class OperationService:
    """Класс описания бизнес логики работы с операциями пользователя"""

    def __init__(self, user) -> None:
        self.user = user
        self.model = Operation

    def create(self, **operation_data) -> Operation:
        """Создание записи операции пользователя"""
        operation = self.model.objects.create(
            user=self.user,
            **operation_data,
        )

        return operation

    def retrieve_list(self, **filters) -> list[Operation | None]:
        """Возвращает список Операций пользователя"""
        qs = self.model.objects.filter(user=self.user)

        for each_filter_key, each_filter_value in filters.items():
            match each_filter_key:
                case "by_operation_type":
                    qs = qs.filter(operation_type=each_filter_value)
                case "by_categories":
                    qs = qs.filter(category_id__in=each_filter_value)
                case "by_operation_start_date":
                    qs = qs.filter(operation_at__gte=each_filter_value)
                case "by_operation_finish_date":
                    qs = qs.filter(operation_at__lte=each_filter_value)
                case _:
                    raise Exception("Неизвестный фильтр")

        return qs.all()

    def retrieve_single(self, operation_id: int) -> Operation | None:
        """Получение одной операции пользователя"""
        try:
            operation = self.model.objects.get(pk=operation_id, user=self.user)
        except self.model.DoesNotExist:
            return None

        return operation

    def update(self, operation_id: int, **operation_data) -> Operation | None:
        """Обновление одной операции"""
        operation = self.retrieve_single(operation_id)
        if not operation:
            return None

        for update_field, update_value in operation_data.items():
            try:
                model_update_field = self.model._meta.get_field(update_field)
            except FieldDoesNotExist:
                break

            setattr(operation, model_update_field.attname, update_value)
        else:
            operation.save()

        return operation

    def delete(self, operation_id: int) -> bool | None:
        """Удаление операции пользователя"""
        operation = self.retrieve_single(operation_id)
        if not operation:
            return None

        operation.delete()

        return True
