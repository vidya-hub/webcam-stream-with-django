from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("cam",views.cam,name="cam"),
    path('video_feed', views.video_feed, name='video_feed'),
]
