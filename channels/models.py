from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 



class Channel(models.Model):
    """

    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='channels', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/', default='../default_post_rgq6aq', blank=True
    )
    followers_count = models.IntegerField(default=0) 

    


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title