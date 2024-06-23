from rest_framework import serializers
from .models import Profile
from channels.models import Channel
from followers.models import Follower
from channels.serializers import ChannelSerializer 

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    followed_channels = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            return request.user == obj.owner
        return False

    def get_following_id(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            user = request.user
            if user.is_authenticated:
                following = Follower.objects.filter(
                    owner=user, followed=obj.owner
                ).first()
                return following.id if following else None
        return None

    def get_followed_channels(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            user = request.user
            if user.is_authenticated:
                followed_channels = Channel.objects.filter(followers__owner=user)
                # You can also add pagination or limit the number of returned channels
                return ChannelSerializer(followed_channels, many=True).data
        return []

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
            'followed_channels',
        ]

    # Ensure you handle cases where certain fields might not be available
    def validate(self, data):
        # Custom validation logic (if needed)
        return data
