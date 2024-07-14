from django.apps import AppConfig


class ApiActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_activity'

    def ready(self) -> None:
        from api_activity import signals