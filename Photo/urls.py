from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import PostView, PostGetUserView, PostGetCreatorView, PhotoManipulateView, PostUpdateDestroyView,StaxMainView, StaxLinkView





urlpatterns = [
    path('post/', PostView.as_view()),
    path('view/post/', PostGetCreatorView.as_view()),
    path('staxcampus/', StaxMainView.as_view()),
    path('linkStax/', StaxLinkView.as_view()),
    path('make/dp/<slug:slug>/', PhotoManipulateView .as_view()),
    path('modify/<int:id>/', PostUpdateDestroyView.as_view()),
    path('<slug:slug>/', PostGetUserView.as_view()),

]