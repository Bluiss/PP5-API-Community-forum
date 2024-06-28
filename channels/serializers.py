from rest_framework import serializers
from channels.models import Channel
from posts.models import Post
from posts.serializers import PostSerializer
from channel_followers.models import ChannelFollower


class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.image.url')
    posts = PostSerializer(
        many=True, read_only=True)  # Assuming posts is a reverse relation
    followers_count = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            follower = ChannelFollower.objects.filter(
                owner=request.user, channel=obj).first()
            return follower.id if follower else None
        return None

    def create(self, validated_data):
        owner = self.context['request'].user
        validated_data['owner'] = owner
        return Channel.objects.create(**validated_data)

    class Meta:
        model = Channel
        fields = [
            'id', 'title', 'description', 'image',
            'is_owner', 'profile_image', 'owner', 'profile_id',
            'posts', 'followers_count', 'following_id',
        ]
