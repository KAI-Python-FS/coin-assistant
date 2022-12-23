
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers
from ..services import BalanceService


class BalanceCurrentView(APIView):
    """Вью работы с текущим Балансом пользователя"""

    def get(self, request: Request) -> Response:
        """Получение текущего баланса пользователя"""
        service = BalanceService(request.user)

        result = service.retrieve_current_balance()

        output_deserialized = serializers.BalanceCurrentOutputSerializer.from_orm(result)

        return Response(
            data=output_deserialized,
        )
