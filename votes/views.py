import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models  
from .models import Vote
from .serializers import VoteSerializer
from posts.models import Post

logger = logging.getLogger(__name__)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        
        logger.debug(f"Received vote request data: {data}")

        try:
            post = Post.objects.get(id=data['post'])
        except Post.DoesNotExist:
            logger.error(f"Post not found with ID: {data['post']}")
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        vote_type = data.get('vote_type')
        if vote_type not in [1, -1]:
            logger.error(f"Invalid vote type: {vote_type}")
            return Response({"detail": "Invalid vote type."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vote, created = Vote.objects.update_or_create(
                user=user,
                post=post,
                defaults={'vote_type': vote_type}
            )

            # Update the post's vote count
            post_vote_count = post.votes.aggregate(total=models.Sum('vote_type'))['total'] or 0
            post.vote_count = post_vote_count
            post.save()

            serializer = self.get_serializer(vote)
            logger.debug(f"Vote created or updated successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error processing vote: {e}")
            return Response({"detail": "An error occurred while processing your request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
