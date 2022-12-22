
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from server.app.base.adapters import query_parameters_to_dict

from . import serializers
from .services import GoalRefillService


class GoalRefillGeneralView(APIView):
    """Вью без привязки к конкретой Цели накопления"""

    def get(self, request: Request) -> Response:
        """Получение списка Целей накопления пользователя"""
        query_params = query_parameters_to_dict(
            request.query_params,
            list_params=("by_categories",)
        )

        try:
            filter_serializer = serializers.GoalRefillListFilterSerializer(**query_params)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = GoalRefillService(user=request.user)
        result = service.retrieve_list(**filter_serializer.dict(exclude_none=True))

        return Response(
            data=[
                serializers.GoalRefillListItemOutputSerializer.from_orm(each_result).dict()
                for each_result in result
            ]
        )

    def post(self, request: Request) -> Response:
        """Добавление Цели накопления пользователем"""
        try:
            serializer = serializers.GoalRefillCreateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = GoalRefillService(user=request.user)
        result = service.create(**serializer.dict(exclude_none=True))

        output_deserialized = serializers.GoalRefillCreateOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
            status=status.HTTP_201_CREATED,
        )