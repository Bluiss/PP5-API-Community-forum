"""
This module contains the admin configuration for the channels application.
"""

from django.contrib import admin
from .models import Channel

# Register your models here.
admin.site.register(Channel)
