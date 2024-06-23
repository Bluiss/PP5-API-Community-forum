from django.urls import path
from channels import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view(), name='channel-list'),
    path('channels/<int:pk>/', views.ChannelDetail.as_view(), name='channel-detail'),
    path('channels/title/<str:title>/', views.ChannelDetailByTitle.as_view(), name='channel-detail-by-title'),
    path('followed/', FollowedChannelsView.as_view(), name='followed-channels'),

]
