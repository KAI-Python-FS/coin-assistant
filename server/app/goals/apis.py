
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from server.app.base.adapters import query_parameters_to_dict
from .services import GoalService


class GoalGeneralView(APIView):
    """Вью без привязки к конкретой Цели"""

    def get(self, request: Request) -> Response:
        """Получение списка целей пользователя"""
        query_params = query_parameters_to_dict(
            request.query_params,
            list_params=("by_categories",)
        )

        service = GoalService(user=request.user)
        result = service.retrieve_list()

        return Response(

        )
