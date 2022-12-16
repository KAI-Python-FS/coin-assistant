
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CategoryCreateInputSerializer, CategoryCreateOutputSerializer
from .services import CategoryService


class CreateCategoryView(APIView):
    """Вью добавления категории"""

    def post(self, request):
        """Добавление категории методом POST"""
        serializer = CategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CategoryService()
        result = service.create(**serializer.validated_data)

        output_serializer = CategoryCreateOutputSerializer(instance=result)

        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )
