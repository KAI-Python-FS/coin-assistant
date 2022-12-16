
from rest_framework import serializers

from .models import Category


class CategoryGetSingleOutputSerializer(serializers.ModelSerializer):
    """Сериализатор исходящих данных получения одной категории"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryCreateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных создания Категории"""

    name = serializers.CharField(required=True)


class CategoryCreateOutputSerializer(CategoryGetSingleOutputSerializer):
    """Сериализатор исходящих данных создания Категории"""