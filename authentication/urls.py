from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import SignUpView, SignUpVerify
urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signup/verify/', SignUpVerify.as_view())
]