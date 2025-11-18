"""
Django AppConfig for the 'newsapp' application.
"""

from django.apps import AppConfig


class NewsappConfig(AppConfig):
    """
    Configuration for the 'newsapp' application.

    This class defines the app's configuration, such as the
    default auto field and the app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsapp"

    def ready(self):
        """
        Executes code when the app registry is fully populated.

        This method is the recommended place to import signals,
        ensuring that they are connected when the app starts.
        """
        # Import signals to connect them to the app's lifecycle
        from . import signals  # noqa: F401
