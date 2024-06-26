"""
This module contains the app configuration for the channels application.
"""

from django.apps import AppConfig

class ChannelsConfig(AppConfig):
    """
    Configuration for the channels application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'channels'
