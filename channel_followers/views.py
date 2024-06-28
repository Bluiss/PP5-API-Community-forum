from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from channels.models import Channel
from .models import ChannelFollower
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)


class FollowChannelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, channel_id):
        try:
            channel = get_object_or_404(Channel, id=channel_id)
            follower, created = ChannelFollower.objects.get_or_create(
                owner=request.user, channel=channel
            )
            if created:
                logger.debug(
                    f'User {request.user.username} followed channel {channel.title}'
                )
                return Response(status=status.HTTP_201_CREATED)
            else:
                logger.debug(
                    f'User {request.user.username} already follows channel {channel.title}'
                )
                return Response(
                    {'detail': 'Already following'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f'Error following channel: {str(e)}')
            return Response(
                {'detail': 'Server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UnfollowChannelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, channel_id):
        try:
            channel = get_object_or_404(Channel, id=channel_id)
            ChannelFollower.objects.filter(
                owner=request.user, channel=channel
            ).delete()
            logger.debug(
                f'User {request.user.username} unfollowed channel {channel.title}'
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Error unfollowing channel: {str(e)}')
            return Response(
                {'detail': 'Server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
