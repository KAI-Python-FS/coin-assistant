
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .services import CategoryService, OperationService


class CategoryGeneralView(APIView):
    """Вью работы без привязки к конкретной Категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoryService()

    def post(self, request):
        """Добавление категории методом POST"""
        try:
            serializer = serializers.CategoryCreateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = self.service.create(**serializer.dict())

        output_deserialized = serializers.CategoryRetrieveOutputSerializer.from_orm(result)
        return Response(
            data=output_deserialized.dict(),
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        """Получение списка категорий"""
        result = self.service.retrieve_list()

        return Response(
            data=[
                serializers.CategoryListItemOutputSerializer.from_orm(each_result).dict()
                for each_result in result
            ],
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

        output_deserialized = serializers.CategoryRetrieveOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
        )

    def put(self, request, category_id: int):
        """Обновление конкретной категории"""
        try:
            serializer = serializers.CategoryUpdateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = self.service.update(
            category_id=category_id,
            **serializer.dict(),
        )
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = serializers.CategoryRetrieveOutputSerializer.from_orm(result)
        return Response(
            data=output_deserialized.dict(),
        )

    def delete(self, request, category_id: int):
        """Удаление конкретной категории"""
        result = self.service.delete(category_id=category_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=result)


class OperationGeneralView(APIView):
    """Вью Категорий без привязки к конкретной Категории"""

    def post(self, request):
        """Добавление операции методом POST"""
        try:
            serializer = serializers.OperationCreateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = OperationService(user=request.user)
        result = service.create(**serializer.dict(exclude_none=True))

        output_deserialized = serializers.OperationCreateOutputSerializer.from_orm(result)
        return Response(
            data=output_deserialized.dict(),
            status=status.HTTP_201_CREATED,
        )


