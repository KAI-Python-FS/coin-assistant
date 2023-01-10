from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers
from ..services import CategoryService


class CategoryGeneralView(APIView):
    """Вью работы без привязки к конкретной Категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = CategoryService()

    def post(self, request: Request) -> Response:
        """Добавление категории методом POST"""
        try:
            serializer = serializers.CategoryCreateInputSerializer.parse_obj(
                request.data
            )
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = self.service.create(serializer.dict())

        output_deserialized = (
            serializers.CategoryRetrieveOutputSerializer.from_orm(result)
        )
        return Response(
            data=output_deserialized.dict(),
            status=status.HTTP_201_CREATED,
        )

    def get(self, request: Request) -> Response:
        """Получение списка категорий"""
        result = self.service.retrieve_list()

        return Response(
            data=[
                serializers.CategoryListItemOutputSerializer.from_orm(
                    each_result
                ).dict()
                for each_result in result
            ],
        )


class CategoryConcreteView(APIView):
    """Вью работы с конкретной записью Категории"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoryService()

    def get(self, request: Request, category_id: int):
        """Получение конкретной категории"""
        result = self.service.retrieve_single(category_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = (
            serializers.CategoryRetrieveOutputSerializer.from_orm(result)
        )

        return Response(
            data=output_deserialized.dict(),
        )

    def put(self, request: Request, category_id: int):
        """Обновление конкретной категории"""
        try:
            serializer = serializers.CategoryUpdateInputSerializer.parse_obj(
                request.data
            )
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = self.service.update(
            category_id,
            **serializer.dict(),
        )
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = (
            serializers.CategoryRetrieveOutputSerializer.from_orm(result)
        )
        return Response(
            data=output_deserialized.dict(),
        )

    def delete(self, request: Request, category_id: int):
        """Удаление конкретной категории"""
        result = self.service.delete(category_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=result)
