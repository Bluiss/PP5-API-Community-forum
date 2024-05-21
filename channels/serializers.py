from rest_framework import serializers
from channels.models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

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
            'is_owner', 'profile_image', 'owner', 'profile_id'
        ]
