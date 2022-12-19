
from pydantic import BaseModel
from rest_framework import serializers

from .models import Category, Operation


class BaseCategorySerializer(BaseModel):
    """Сериализатор всех данных одной категории"""

    id: int
    name: str

    class Config:
        orm_mode = True

class CategoryRetrieveOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных получения одной категории"""

    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryListOutputSerializer(BaseModel):
    """Сериализатор получения списка Категорий"""

    __root__: list[BaseCategorySerializer]

    class Config:
        orm_mode = True


class CategoryCreateInputSerializer(BaseModel):
    """Сериализатор входящих данных создания Категории"""

    name: str


class CategoryCreateOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных создания Категории"""


class CategoryUpdateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных обновления Категории"""

    name: str


class CategoryUpdateOutputSerializer(BaseCategorySerializer):
    """Сериалиазатор исходящих данных обновления Категории"""


class OperationRetrieveOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation


class OperationCreateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных создания Операции пользователя"""

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    operation_at = serializers.DateTimeField(required=False)
    operation_type = serializers.CharField(required=True)
    cost = serializers.FloatField(required=True)
    category = serializers.IntegerField(required=False)


class OperationCreateOutputSerializer(serializers.Serializer):
    """Сериализатор исходящих данных создания Операции пользователя"""
