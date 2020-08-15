from django.apps import AppConfig


class SiteuserConfig(AppConfig):
    name = 'siteuser'
    
    def ready(self):
            from . import signals # noqa
