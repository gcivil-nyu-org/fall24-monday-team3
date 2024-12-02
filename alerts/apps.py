from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alerts"

    def ready(self):
        import alerts.signals   # noqa: F401 - Import necessary to activate signals
