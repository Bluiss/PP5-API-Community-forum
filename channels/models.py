from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    """
    
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='channels')
    image = models.ImageField(
        upload_to='images/', default='../default_post_rgq6aq', blank=True
    )


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'