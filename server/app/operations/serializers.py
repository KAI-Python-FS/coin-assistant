
from rest_framework import serializers


class CategoryGetSingleOutputSerializer(serializers.Serializer):
    """Сериализатор исходящих данных получения одной категории"""

    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


class CategoryCreateInputSerializer(serializers.Serializer):
    """Сериализатор входящих данных создания Категории"""

    name = serializers.CharField(required=True)


class CategoryCreateOutputSerializer(CategoryGetSingleOutputSerializer):
    """Сериализатор исходящих данных создания Категории"""