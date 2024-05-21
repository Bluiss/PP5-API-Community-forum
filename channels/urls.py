from django.urls import path
from channels import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view()),
]