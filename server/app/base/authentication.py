from rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    """Кастомизация ключевого слова в заголовке запроса"""

    keyword = 'Bearer'
