from django.urls import path, include
from rest_framework import routers

from app.views import AuthViewSet, ProfileViewSet
from app.views.user import UserViewSet


api_router = routers.DefaultRouter()
api_router.register(r'auth', AuthViewSet, basename='auth')
api_router.register(r'profile', ProfileViewSet, basename='profile')
api_router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(api_router.urls))
]
