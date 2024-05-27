from rest_framework import serializers
from posts.models import Post, Channel
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    channel_title = serializers.CharField(write_only=True)
    channel_display_title = serializers.ReadOnlyField(source='channel.title')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    def create(self, validated_data):
        channel_title = validated_data.pop('channel_title')
        try:
            channel = Channel.objects.get(title=channel_title)
        except Channel.DoesNotExist:
            raise serializers.ValidationError({'channel': 'Channel not found.'})
        validated_data['channel'] = channel
        post = Post.objects.create(**validated_data)
        return post

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'channel_title',
            'channel_display_title', 'image_filter', 'like_id', 
            'likes_count', 'comments_count',
        ]
