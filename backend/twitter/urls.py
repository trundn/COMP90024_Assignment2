from django.urls import path, include
from .views import TwitterViewSet
from rest_framework.routers import DefaultRouter

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    path('', include(twitter_router.urls))
]
