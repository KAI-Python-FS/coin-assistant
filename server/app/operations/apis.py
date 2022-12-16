
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .services import CategoryService


class CategoryGeneralView(APIView):
    """Вью работы без привязки к конкретной Категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoryService()

    def post(self, request):
        """Добавление категории методом POST"""
        serializer = serializers.CategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.service.create(**serializer.validated_data)

        output_serializer = serializers.CategoryCreateOutputSerializer(instance=result)

        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        """Получение списка категорий"""
        result = self.service.retrieve_list()

        output_serializer = serializers.CategoryListOutputSerializer(
            instance=result,
            many=True,
        )

        return Response(
            data=output_serializer.data,
        )


class CategoryConcreteView(APIView):
    """Вью работы с конкретной записью Категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoryService()

    def get(self, request, category_id: int):
        """Получение конкретной категории"""
        result = self.service.retrieve_single(category_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_serializer = serializers.CategoryRetrieveOutputSerializer(
            instance=result
        )
        return Response(
            data=output_serializer.data,
        )

    def put(self, request, category_id: int):
        """Обновление конкретной категории"""
        serializer = serializers.CategoryUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.service.update(
            category_id=category_id,
            **serializer.validated_data,
        )
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_serializer = serializers.CategoryUpdateOutputSerializer(
            instance=result
        )
        return Response(
            data=output_serializer.data,
        )
