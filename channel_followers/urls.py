from django.urls import path
from .views import FollowChannelView, UnfollowChannelView

urlpatterns = [
    path('channels/<int:channel_id>/follow/', FollowChannelView.as_view(), name='follow-channel'),
    path('channels/<int:channel_id>/unfollow/', UnfollowChannelView.as_view(), name='unfollow-channel'),
]