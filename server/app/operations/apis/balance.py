
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import BalanceService


class BalanceCurrentView(APIView):
    """Вью работы с текущим Балансом пользователя"""

    def get(self, request: Request) -> Response:
        """Получение текущего баланса пользователя"""
        service = BalanceService(request.user)

        result = service.retrieve_current_balance()

        return Response(data=result)


class BalanceDetailedView(APIView):
    """Вью работы с детализацией Баланса пользователя"""

    def get(self, request: Request) -> Response:
        """Получение детализированной информации о Балансе пользователя"""
        service = BalanceService(request.user)

        result = service.retrieve_current_balance_detailed()

        return Response(data=result)
