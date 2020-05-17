from django.urls import path, include
from .views import TwitterViewSet, TweetsPerHourView, LanguageStatisticsView
from rest_framework.routers import DefaultRouter

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    path('tweets-per-hour/', TweetsPerHourView.as_view()),
    path('language-statistics/', LanguageStatisticsView.as_view()),
    path('document/', include(twitter_router.urls))
]
