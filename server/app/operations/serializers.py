
from rest_framework import serializers

from .models import Category


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
    """Сериалиазтор исходящих данных обновления Категории"""
