from django.apps import AppConfig


class NewsmanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Newsman'

    def ready(self):
        import Newsman.signals