from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

# Use get_model to reference the Post and Vote models dynamically
Post = apps.get_model('posts', 'Post')
Vote = apps.get_model('votes', 'Vote')

@receiver(post_save, sender=Vote)
def update_vote_count_on_save(sender, instance, created, **kwargs):
    post = instance.post
    if created:
        post.vote_count += instance.vote_type
    else:
        # Handle the case where vote_type might change
        old_vote_type = Vote.objects.filter(pk=instance.pk).values('vote_type').first()['vote_type']
        post.vote_count += instance.vote_type - old_vote_type
    post.save()

@receiver(post_delete, sender=Vote)
def update_vote_count_on_delete(sender, instance, **kwargs):
    post = instance.post
    post.vote_count -= instance.vote_type
    post.save()
