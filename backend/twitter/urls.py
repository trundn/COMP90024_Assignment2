from django.urls import path, include
from .views import TwitterViewSet, TweetsPerHourView, LanguageStatisticsView, TweetsInRectangleView, \
    TweetsInPolygonView, StatisticsInPolygonView
from rest_framework.routers import DefaultRouter

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    path('tweets-per-hour/', TweetsPerHourView.as_view()),
    path('language-statistics/', LanguageStatisticsView.as_view()),
    path('tweets-in-rectangle/', TweetsInRectangleView.as_view()),
    path('tweets-in-polygon/', TweetsInPolygonView.as_view()),
    path('statistics-in-polygon/', StatisticsInPolygonView.as_view()),
    path('document/', include(twitter_router.urls))
]
