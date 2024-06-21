from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vote
from .serializers import VoteSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        post = Post.objects.get(id=data['post'])
        vote_type = data['vote_type']

        vote, created = Vote.objects.update_or_create(
            user=user,
            post=post,
            defaults={'vote_type': vote_type}
        )

        # Recalculate the vote count for the post
        post.vote_count = post.votes.aggregate(models.Sum('vote_type'))['vote_type__sum'] or 0
        post.save()

        serializer = self.get_serializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
