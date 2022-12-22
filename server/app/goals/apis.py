
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from server.app.base.adapters import query_parameters_to_dict

from . import serializers
from .services import BudgetService, GoalRefillService


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


class GoalRefillConcreteView(APIView):
    """Вью работы с конкретной записью Цели накопления"""

    def get(self, request: Request, goal_id: int) -> Response:
        """Получение конкретной Цели накопления"""
        service = GoalRefillService(user=request.user)

        result = service.retrieve_single(goal_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = serializers.GoalRefillRetrieveOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
        )

    def put(self, request: Request, goal_id: int) -> Response:
        """Обновление конкретной Цели пользователя"""
        try:
            serializer = serializers.GoalRefillUpdateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = GoalRefillService(user=request.user)
        result = service.update(
            goal_id,
            **serializer.dict(exclude_none=True),
        )
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        output_deserialized = serializers.GoalRefillUpdateOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
        )

    def delete(self, request: Request, goal_id: int) -> Response:
        """Удаление конкретной Цели пользователя"""
        service = GoalRefillService(user=request.user)

        result = service.delete(goal_id)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=result)


class BudgetGeneralView(APIView):
    """Вью без привязки к конкретному Бюджету пользователя"""

    def get(self, request: Request) -> Response:
        """Получение списка Бюджетов пользователя"""
        query_params = query_parameters_to_dict(
            request.query_params,
            list_params=("by_categories",)
        )

        try:
            filter_serializer = serializers.BudgetListFilterSerializer(**query_params)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = BudgetService(user=request.user)
        result = service.retrieve_list(**filter_serializer.dict(exclude_none=True))

        return Response(
            data=[
                serializers.BudgetListItemOutputSerializer.from_orm(each_result).dict()
                for each_result in result
            ]
        )

    def post(self, request: Request) -> Response:
        """Добавление Бюджета пользователя"""
        try:
            serializer = serializers.BudgetCreateInputSerializer.parse_obj(request.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = BudgetService(user=request.user)
        result = service.create(**serializer.dict(exclude_none=True))

        output_deserialized = serializers.BudgetCreateOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized.dict(),
            status=status.HTTP_201_CREATED,
        )
