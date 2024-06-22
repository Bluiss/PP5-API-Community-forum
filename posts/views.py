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
    
    # Annotate the queryset with likes_count, comments_count, and vote_count
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        total_vote_count=Sum(F('votes__vote_type'), distinct=True)  # Using a different name for the annotation
    ).order_by('-created_at')  # Default ordering

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = [
        'owner__followed__owner__profile',  # To filter posts by profiles followed by the user
        'likes__owner__profile',  # To filter posts liked by a profile
        'owner__profile',  # To filter posts by the owner’s profile
        'channel',  # To filter posts by channel
    ]
    
    search_fields = [
        'owner__username',
        'title',
        'channel__title',
    ]
    
    ordering_fields = [
        'created_at',  # Sorting by the creation date
        'likes_count',  # Sorting by the number of likes
        'comments_count',  # Sorting by the number of comments
        'vote_count',  # Sorting by the vote count
        'updated_at',  # Sorting by the last update date
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