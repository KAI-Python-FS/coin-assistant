
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'server.app.base.authentication.BearerAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
