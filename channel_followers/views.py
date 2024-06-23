# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ChannelFollower, Channel
from .serializers import ChannelFollowerSerializer

class FollowChannelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChannelFollowerSerializer

    def post(self, request, channel_id):
        try:
            # Ensure the channel exists
            channel = get_object_or_404(Channel, id=channel_id)
            print(f"Channel found: {channel.title}")

            # Create the ChannelFollower instance using the serializer
            data = {
                'owner': request.user.username,  # assuming user is an instance of User
                'channel': channel.title,
                'created_at': None  # The created_at will be auto-handled by the model
            }
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            # Create or get the ChannelFollower instance
            follower, created = ChannelFollower.objects.get_or_create(
                owner=request.user, channel=channel
            )
            print(f"ChannelFollower created: {created}")

            # Use serializer to serialize the response data
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except serializers.ValidationError as ve:
            # Handle validation errors gracefully
            print(f"Validation error: {ve}")
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the exception details for debugging
            print(f"Error in FollowChannelView: {str(e)}")
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnfollowChannelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        try:
            # Ensure the channel exists
            channel = get_object_or_404(Channel, id=channel_id)
            print(f"Channel found for unfollow: {channel.title}")

            # Attempt to delete the ChannelFollower entry
            result = ChannelFollower.objects.filter(owner=request.user, channel=channel).delete()
            print(f"ChannelFollower deleted: {result}")

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Log the exception details for debugging
            print(f"Error in UnfollowChannelView: {str(e)}")
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
