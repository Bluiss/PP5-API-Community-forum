import logging
from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

# Configure logging
logger = logging.getLogger(__name__)

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    def get_queryset(self):
        try:
            # Log the request details
            logger.debug("Processing ProfileList view request")

            queryset = Profile.objects.annotate(
                posts_count=Count('owner__post', distinct=True),
                followers_count=Count('owner__followed', distinct=True),
                following_count=Count('owner__following', distinct=True)
            ).order_by('-created_at')

            # Log the success and details of the queryset
            logger.debug(f"ProfileList queryset generated: {queryset.query}")

            return queryset
        except Exception as e:
            # Log any exceptions that occur
            logger.error(f"Error in ProfileList view: {str(e)}")
            raise

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        try:
            # Log the request details
            logger.debug("Processing ProfileDetail view request")

            queryset = Profile.objects.annotate(
                posts_count=Count('owner__post', distinct=True),
                followers_count=Count('owner__followed', distinct=True),
                following_count=Count('owner__following', distinct=True)
            ).order_by('-created_at')

            # Log the success and details of the queryset
            logger.debug(f"ProfileDetail queryset generated: {queryset.query}")

            return queryset
        except Exception as e:
            # Log any exceptions that occur
            logger.error(f"Error in ProfileDetail view: {str(e)}")
            raise
