# Generated by Django 3.2 on 2024-06-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_followers_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
