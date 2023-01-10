from typing import Any, Type

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model, Q
from django.db.models.query import QuerySet


class InterfaceCRUDService:
    """
    Базовый класс описания CRUD-логики.
    Служит для определения интерфейса сервисов
    """

    def create(self, *args, **object_data) -> Any:
        """Создание объекта"""
        raise NotImplementedError

    def retrieve_single(self, object_id: int, *args, **kwargs) -> Any:
        """Получение одной объекта"""
        raise NotImplementedError

    def retrieve_list(self, *args, **filters) -> Any:
        """Получение списка объектов"""
        raise NotImplementedError

    def update(self, object_id: int, **object_data) -> Any:
        """Обновление объекта"""
        raise NotImplementedError

    def delete(self, object_id: int, **kwargs) -> Any:
        """Удаление объекта"""
        raise NotImplementedError


class BaseModelCRUDService(InterfaceCRUDService):
    """Базовый класс описания CRUD-логики на основе модели"""

    model: Type[Model]

    def _filters_retrieve_single(self, object_id: int) -> Q:
        """Возвращает фильтры получения конкретной записи объекта"""
        return Q(pk=object_id)

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает фильтры получения конкретной списка объектов согласно фильтрам"""
        return Q()

    def _get_qs_retrieve_single(self, object_id: int) -> QuerySet:
        """Возвращает кварисет получения конкретной записи объекта"""
        qs_filters = self._filters_retrieve_single(object_id)

        return self.model.objects.filter(qs_filters)

    def _get_qs_retrieve_list(self, **filters) -> QuerySet:
        """Возвращает кварисет получения списка записей объекта"""
        # TODO добавить select_related в связанных моделях
        qs_filters = self._filters_retrieve_list(**filters)

        return self.model.objects.filter(qs_filters).all()

    def create(self, object_data: dict[str, Any], *args, **kwargs) -> Model:
        """Создание объекта"""
        object_ = self.model.objects.create(**object_data)
        object_.full_clean()

        return object_

    def retrieve_single(self, object_id: int, *args, **kwargs) -> Model | None:
        """Получение конкретного объекта по PK"""
        try:
            object_ = self._get_qs_retrieve_single(object_id).get()
        except self.model.DoesNotExist:
            return None

        return object_

    def retrieve_list(self, *args, **filters: dict[str, Any]) -> QuerySet:
        """Возвращает список объектов согласно фильтрам"""
        return self._get_qs_retrieve_list(**filters).all()  # type: ignore

    def update(self, object_id: int, **object_data) -> Model | None:
        """Обновляет конкретный объект"""
        object_ = self.retrieve_single(object_id)
        if not object_:
            return None

        for update_field_name, update_value in object_data.items():
            try:
                model_update_field = self.model._meta.get_field(  # type: ignore
                    update_field_name
                )
            except FieldDoesNotExist:
                break

            # Обновление только изменившихся данных
            current_value = getattr(object_, model_update_field.attname)  # type: ignore
            if current_value != update_value:
                setattr(object_, model_update_field.attname, update_value)  # type: ignore
        else:
            object_.full_clean()
            object_.save()

        return object_

    def delete(self, object_id: int, **kwargs) -> bool | None:
        """Удаляет конкретный объекта"""
        object_ = self.retrieve_single(object_id)
        if not object_:
            return None

        object_.delete()

        return True


class BaseModelUserFilterCRUDService(BaseModelCRUDService):
    """Примесь, добавляющая фильтрацию по пользователю"""

    def __init__(self, user):
        super().__init__()

        self.user = user

    def _filters_retrieve_single(self, object_id: int) -> Q:
        """Возвращает фильтры получения конкретной записи объекта"""
        return Q(
            pk=object_id,
            user=self.user,
        )

    def _filters_retrieve_list(self, **filters) -> Q:
        """Возвращает фильтры получения конкретной списка объектов согласно фильтрам"""
        return Q(user=self.user)

    def create(self, object_data: dict[Any, Any], *args, **kwargs) -> Model:
        """Создание объекта"""
        object_data.update({
            "user": self.user
        })
        return super().create(object_data, *args, **kwargs)
