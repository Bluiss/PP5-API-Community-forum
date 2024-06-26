"""
This module contains the models for the channels application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Channel(models.Model):
    """
    This model represents a channel in the community forum.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='channels', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/', default='../default_post_rgq6aq', blank=True
    )

    @property
    def followers_count(self):
        """
        Returns the number of followers for the channel.
        """
        return ChannelFollower.objects.filter(channel=self).count()

    class Meta:
        """
        Meta options for the Channel model.
        """
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)
