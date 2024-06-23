from django.db import models
from django.contrib.auth.models import User
from channels.models import Channel  

class ChannelFollower(models.Model):
    """
    ChannelFollower model, related to 'owner' and 'channel'.
    'owner' is a user that is following a Channel.
    'channel' is a Channel that is followed by 'owner'.
    We need the related_name attribute so that django can differentiate
    between 'owner' and 'channel'.
    'unique_together' makes sure a user can't 'double follow' the same channel.
    """
    owner = models.ForeignKey(
        User, related_name='channel_following', on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        Channel, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'channel']

    def __str__(self):
        return f'{self.owner.username} follows {self.channel.title}'
