# Generated by Django 3.2 on 2024-06-21 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_post_followers_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'vote_type', models.SmallIntegerField(
                        choices=[(1, 'Upvote'), (-1, 'Downvote')]
                    )
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'post', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='votes', to='posts.post'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]
