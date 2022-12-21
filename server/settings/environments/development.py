"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

from typing import List

from server.settings.components.common import (
    ALLOWED_HOSTS,
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
)

# Setting the development status:

DEBUG = True
# Для возможности выполнения запросов с web-интерфейса Swagger
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS += [
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
    '29d1-94-180-176-227.ngrok.io',
]


# Installed apps for development only:

INSTALLED_APPS += (
    # Better debug:
    # 'debug_toolbar',
)


# Static files:
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS: List[str] = []

# Disable persistent DB connections
# https://docs.djangoproject.com/en/3.2/ref/databases/#caveats
DATABASES['default']['CONN_MAX_AGE'] = 0
