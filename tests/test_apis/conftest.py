import pytest
# from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from tests.factories.user import UserFactory

User = get_user_model()


@pytest.fixture
def api_user():
    return UserFactory.create()


@pytest.fixture
def api_client_authorized(api_user) -> APIClient:
    """Возвращает клиент для работы с API"""
    client = APIClient()

    user_token = api_user.auth_token.key

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")

    return client
