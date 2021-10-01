"""
Apps.py contains the configuration of Post app
"""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    PostsConfig class extends AppConfig that store metadata for Posts application
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.posts"
