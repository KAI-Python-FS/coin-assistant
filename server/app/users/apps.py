from django.apps import AppConfig

# pylint: disable=C0415 W0611


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.app.users"

    def ready(self):
        from .receivers import create_auth_token  # noqa
