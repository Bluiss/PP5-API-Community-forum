from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Channel
from .serializers import ChannelSerializer
from rest_framework.filters import OrderingFilter

class ChannelList(APIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        channels = Channel.objects.all()
        serializer = ChannelSerializer(channels, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ChannelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        return queryset.order_by(self.request.query_params.get('ordering', '-created_at'))

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Channel
from .serializers import ChannelSerializer
import logging

logger = logging.getLogger(__name__)

class ChannelDetailByTitle(generics.RetrieveAPIView):
    serializer_class = ChannelSerializer

    def get_object(self):
        title = self.kwargs.get("title")
        logger.debug(f'Received request for channel title: {title}')
        try:
            channel = Channel.objects.get(title=title)
            logger.debug(f'Found channel: {channel}')
            return channel
        except Channel.DoesNotExist:
            logger.error(f'Channel with title "{title}" not found.')
            raise Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

