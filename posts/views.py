from django.db.models import Count, Sum, F, Value
from rest_framework import generics, permissions, filters, viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        total_vote_count=Sum(F('votes__vote_type'), distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = {
        'owner__followed__owner__profile': ['exact'],  
        'likes__owner__profile': ['exact'],  
        'owner__profile': ['exact'],  
        'channel__title': ['exact'],  # Use channel__title to filter by channel title
    }
    
    search_fields = [
        'owner__username',
        'title',
        'channel__title',
    ]
    
    ordering_fields = [
        'created_at',
        'likes_count',
        'comments_count',
        'total_vote_count',  # Use total_vote_count here
        'updated_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['channel__id']  