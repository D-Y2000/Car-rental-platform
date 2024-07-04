from django.apps import AppConfig


class ApiDestinationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_destination'

    def ready(self) -> None:
        from api_destination import signals