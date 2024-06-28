from rest_framework import serializers
from django.db import models
from .models import Vote
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'image', 'channel', 'image_filter',
            'followers_count', 'created_at', 'updated_at', 'vote_count'
        ]

    def get_vote_count(self, obj):
        return obj.votes.aggregate(
            models.Sum('vote_type')
        )['vote_type__sum'] or 0


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'post', 'vote_type', 'created_at']
