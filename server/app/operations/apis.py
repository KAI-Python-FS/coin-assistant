
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .services import CategoryService


class ListCreateCategoryView(APIView):
    """Вью добавления категории и получения списка категорий"""

    def post(self, request):
        """Добавление категории методом POST"""
        serializer = serializers.CategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CategoryService()
        result = service.create(**serializer.validated_data)

        output_serializer = serializers.CategoryCreateOutputSerializer(instance=result)

        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        """Получение списка категорий"""
        service = CategoryService()

        result = service.retrieve_list()

        output_serializer = serializers.CategoryListOutputSerializer(
            instance=result,
            many=True,
        )

        return Response(
            data=output_serializer.data,
        )