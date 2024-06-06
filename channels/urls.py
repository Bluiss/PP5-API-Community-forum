from django.urls import path
from channels import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view()),
    path('channels/<int:pk>', views.ChannelDetail.as_view()),

]