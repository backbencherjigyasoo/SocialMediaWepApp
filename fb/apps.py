from django.apps import AppConfig


class FbConfig(AppConfig):
    name = 'fb'

    def ready(self):
        import fb.mysignal
