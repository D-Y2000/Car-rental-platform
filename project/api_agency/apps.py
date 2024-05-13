from django.apps import AppConfig


class ApiAgencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_agency'
    

    def ready(self) -> None:
        from api_agency import signals