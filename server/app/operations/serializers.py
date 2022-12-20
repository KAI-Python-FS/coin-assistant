import datetime

from pydantic import BaseModel
from rest_framework import serializers

from .enums import OperationTypeEnum
from .models import Category, Operation


class BaseCategorySerializer(BaseModel):
    """Сериализатор всех данных одной категории"""

    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryRetrieveOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных получения одной категории"""


class CategoryListItemOutputSerializer(BaseCategorySerializer):
    """Сериализатор получения списка Категорий"""


class CategoryCreateInputSerializer(BaseModel):
    """Сериализатор входящих данных создания Категории"""

    name: str


class CategoryCreateOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных создания Категории"""


class CategoryUpdateInputSerializer(BaseModel):
    """Сериализатор входящих данных обновления Категории"""

    name: str


class CategoryUpdateOutputSerializer(BaseCategorySerializer):
    """Сериалиазатор исходящих данных обновления Категории"""


class BaseOperationSerializer(BaseModel):
    """Сериализатор всех данных одной операции"""

    id: int
    name: str
    description: str | None
    operation_at: datetime.datetime | None
    operation_type: OperationTypeEnum
    cost: float
    category: BaseCategorySerializer | None

    class Config:
        orm_mode = True


class OperationCreateInputSerializer(BaseOperationSerializer):
    """Сериализатор входящих данных создания Операции пользователя"""


class OperationCreateOutputSerializer(BaseOperationSerializer):
    """Сериализатор исходящих данных создания Операции пользователя"""
