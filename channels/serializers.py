from rest_framework import serializers
from channels.models import Channel
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'created_at', 'updated_at', 'channel']

class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    posts = PostSerializer(many=True, read_only=True)
    followers_count = serializers.SerializerMethodField()  # Ensure this field is correctly linked

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_followers_count(self, obj):
        return obj.followers.count()  # Correctly returns the count of followers

    def create(self, validated_data):
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
