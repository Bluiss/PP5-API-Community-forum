from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Channel
from .serializers import ChannelSerializer
from rest_framework.filters import OrderingFilter
import logging
from django.shortcuts import get_object_or_404
from django.http import Http404

logger = logging.getLogger(__name__)


class ChannelList(APIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        channels = Channel.objects.all()
        serializer = ChannelSerializer(
            channels, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ChannelSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f'Error creating channel: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['followers_count']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(
            self.request.query_params.get('ordering', '-created_at'))


class ChannelDetailByTitle(RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'title'

    def get_object(self):
        title = self.kwargs.get("title")
        logger.debug(f'Received request for channel title: {title}')
        channel = get_object_or_404(Channel, title=title)
        logger.debug(f'Found channel: {channel}')
        return channel

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            logger.error(
                f'Channel with title "{self.kwargs.get("title")}" not found.')
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class FollowedChannelsView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(followers__owner=user)
