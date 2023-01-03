import pytest

from tests.factories.user import UserFactory


class TestAuthTokenCreateBySignal:
    """Тест для проверки создания токена авторизации пользователя"""

    @pytest.mark.django_db()
    def test_create(self):
        """Проверка генерации токена пользователя"""
        user = UserFactory.create()

        assert user.auth_token.key
