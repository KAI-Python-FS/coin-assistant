
from rest_framework import serializers

from .models import Category, Operation


class CategoryRetrieveOutputSerializer(serializers.ModelSerializer):
    """Сериализатор исходящих данных получения одной категории"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryListOutputSerializer(CategoryRetrieveOutputSerializer):
    """Сериализатор получения списка Категорий"""


class CategoryCreateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных создания Категории"""

    name = serializers.CharField(required=True)


class CategoryCreateOutputSerializer(CategoryRetrieveOutputSerializer):
    """Сериализатор исходящих данных создания Категории"""


class CategoryUpdateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных обновления Категории"""

    name = serializers.CharField(required=True)


class CategoryUpdateOutputSerializer(CategoryRetrieveOutputSerializer):
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
