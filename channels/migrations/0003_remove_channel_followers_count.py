# Generated by Django 3.2 on 2024-06-23 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0002_alter_channel_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='followers_count',
        ),
    ]