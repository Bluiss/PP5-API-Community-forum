from rest_framework import serializers
from channels.models import Channel
from posts.models import Post
from posts.serializers import PostSerializer  # Ensure you have this imported correctly
from followers.models import ChannelFollower  # Ensure you have the correct import for ChannelFollower

class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Read-only field for owner's username
    is_owner = serializers.SerializerMethodField()  # Custom method to check if current user is the owner
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')  # Read-only field for owner's profile ID
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')  # Read-only field for profile image URL
    posts = PostSerializer(many=True, read_only=True)  # Nested serializer for posts related to the channel
    followers_count = serializers.SerializerMethodField()  # Custom method to get the count of followers

    def get_is_owner(self, obj):
        # Check if the current request user is the owner of the channel
        request = self.context['request']
        return request.user == obj.owner

    def get_followers_count(self, obj):
        # Return the count of followers for the channel using the related name 'followers'
        return obj.followers.count()

    def create(self, validated_data):
        # Set the owner of the channel to the current request user
        owner = self.context['request'].user
        validated_data['owner'] = owner
        return Channel.objects.create(**validated_data)

    class Meta:
        model = Channel
        fields = [
            'id', 'title', 'description', 'image',
            'is_owner', 'profile_image', 'owner', 'profile_id',
            'posts', 'followers_count'
        ]
