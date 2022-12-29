from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from server.app.base.adapters import query_parameters_to_dict
from .. import serializers
from ..services import OperationService


class OperationGeneralView(APIView):
    """Вью Категорий без привязки к конкретной Категории"""

    def post(self, request: Request) -> Response:
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

    def get(self, request: Request) -> Response:
        """Получение списка Операций"""
        query_params = query_parameters_to_dict(
            request.query_params,
            list_params=("by_categories",)
        )
        try:
            filter_serializer = serializers.OperationListFilterSerializer(**query_params)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = OperationService(user=request.user)
        result = service.retrieve_list(**filter_serializer.dict(exclude_none=True))

        return Response(
            data=[
                serializers.OperationListItemOutputSerializer.from_orm(each_result).dict()
                for each_result in result
            ],
        )


class OperationConcreteView(APIView):
    """Вью работы с конкретной записью Операции"""

    def get(self, request: Request, operation_id: int) -> Response:
        """Получение конкретной операции"""
        service = OperationService(user=request.user)

        result = service.retrieve_single(operation_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = serializers.OperationRetrieveOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
        )

    def put(self, request: Request, operation_id: int) -> Response:
        """Обновление конкретной операции"""
        try:
            serializer = serializers.OperationUpdateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = OperationService(user=request.user)
        result = service.update(operation_id, **serializer.dict(exclude_unset=True))
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = serializers.OperationRetrieveOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
        )

    def delete(self, request: Request, operation_id: int) -> Response:
        """Удаление конкретной операции"""
        service = OperationService(user=request.user)

        result = service.delete(operation_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=result)
