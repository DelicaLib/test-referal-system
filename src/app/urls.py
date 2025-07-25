from django.urls import path, include
from rest_framework import routers

from app.views import AuthViewSet


api_router = routers.DefaultRouter()
api_router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(api_router.urls))
]
