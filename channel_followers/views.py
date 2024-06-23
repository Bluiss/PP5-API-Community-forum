from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ChannelFollower
from .serializers import ChannelFollowerSerializer


class FollowChannelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        ChannelFollower.objects.get_or_create(user=request.user, channel=channel)
        return Response(status=status.HTTP_201_CREATED)

class UnfollowChannelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        ChannelFollower.objects.filter(user=request.user, channel=channel).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)