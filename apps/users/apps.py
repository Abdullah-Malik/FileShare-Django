"""
users.app file containing the configuration of app
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    UsersConfig class extends AppConfig that store metadata for an application
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
