from django.urls import path, include
from .views import PolygonViewSet, TwitterViewSet, TweetsPerHourView, TotalTweetsByDayAndHour, LanguageStatisticsView, \
    TweetsWithEmoValuesAndProCnt, TweetsInRectangleView, TweetsInPolygonView, StatisticsInPolygonView, FindRouteView, \
    GetMostActiveUsersView, GetUserInfoView, TweetsByCategoriesView, TweetsWithCoordinatesView, MovementView
from rest_framework.routers import DefaultRouter

polygon_router = DefaultRouter()
polygon_router.register('', PolygonViewSet)

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    # urls for Home
    path('tweets-by-categories/', TweetsByCategoriesView.as_view()),
    path('tweets-with-coordinates/', TweetsWithCoordinatesView.as_view()),

    # sentiment
    path('polygon/', include(polygon_router.urls)),
    path('tweets-in-rectangle/', TweetsInRectangleView.as_view()),
    path('tweets-in-polygon/', TweetsInPolygonView.as_view()),
    path('statistics-in-polygon/<pk>/', StatisticsInPolygonView.as_view()),
    path('statistics-in-polygon/', StatisticsInPolygonView.as_view()),

    # sentiment analysis
    path('tweets-with-emo-values-and-pro-cnt/', TweetsWithEmoValuesAndProCnt.as_view()),

    # movement
    path('movement/', MovementView.as_view()),

    # user tracker
    path('find-route/', FindRouteView.as_view()),
    path('get-most-active-users/', GetMostActiveUsersView.as_view()),
    path('get-user-info/<pk>', GetUserInfoView.as_view()),

    # statistics
    path('tweets-per-hour/', TweetsPerHourView.as_view()),
    path('language-statistics/', LanguageStatisticsView.as_view()),
    path('total-tweets-by-day-and-hour/', TotalTweetsByDayAndHour.as_view()),

    path('document/', include(twitter_router.urls))
]
