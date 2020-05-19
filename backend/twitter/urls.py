from django.urls import path, include
from .views import PolygonViewSet, TwitterViewSet, TweetsPerHourView, LanguageStatisticsView, TweetsInRectangleView, \
    TweetsInPolygonView, StatisticsInPolygonView, FindRouteView
from rest_framework.routers import DefaultRouter

polygon_router = DefaultRouter()
polygon_router.register('', PolygonViewSet)

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    path('polygon/', include(polygon_router.urls)),
    path('tweets-per-hour/', TweetsPerHourView.as_view()),
    path('language-statistics/', LanguageStatisticsView.as_view()),
    path('tweets-in-rectangle/', TweetsInRectangleView.as_view()),
    path('tweets-in-polygon/', TweetsInPolygonView.as_view()),
    path('statistics-in-polygon/<pk>/', StatisticsInPolygonView.as_view()),
    path('find-route/', FindRouteView.as_view()),
    path('document/', include(twitter_router.urls))
]
