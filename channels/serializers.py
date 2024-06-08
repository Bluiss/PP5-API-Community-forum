from rest_framework import serializers
from channels.models import Channel
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'created_at', 'updated_at', 'channel', 'followers_count']


class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    posts = PostSerializer(many=True, read_only=True)  # Include the related posts

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def create(self, validated_data):
        owner = self.context['request'].user
        validated_data['owner'] = owner
        return Channel.objects.create(**validated_data)

    class Meta:
        model = Channel
        fields = [
            'id', 'title', 'description', 'image',
            'is_owner', 'profile_image', 'owner', 'profile_id',
            'posts'  
            ]
