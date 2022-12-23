
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import BalanceService
from .. import serializers


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

        output_deserialized = serializers.BalanceDetailedOutputSerializer(
            balance=result.balance,
            refill=[
                serializers.BalanceDetailedCategoryOutputSerializer(
                    category_id=each_refill.category_id,
                    category_name=each_refill.category_name,
                    total=each_refill.total,
                )
                for each_refill in result.refill
            ],
            spending=[
                serializers.BalanceDetailedCategoryOutputSerializer(
                    category_id=each_refill.category_id,
                    category_name=each_refill.category_name,
                    total=each_refill.total,
                )
                for each_refill in result.spending
            ],
        )

        return Response(data=output_deserialized.dict())
