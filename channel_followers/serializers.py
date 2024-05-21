from rest_framework import serializers
from channel_followers.models import ChannelFollower



class ChannelFollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'owner' and 'followed'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    channel = serializers.ReadOnlyField(source='channel.title')

    class Meta:
        model = ChannelFollower
        fields = ['id', 'owner', 'channel', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})