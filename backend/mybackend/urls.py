from django.urls import path, include
from .views import ArticleViewSet, TwitterViewSet
from rest_framework.routers import DefaultRouter

article_router = DefaultRouter()
article_router.register('', ArticleViewSet, basename='article')

twitter_router = DefaultRouter()
twitter_router.register('', TwitterViewSet, basename='twitter')

urlpatterns = [
    path('article/', include(article_router.urls)),
    path('twitter/', include(twitter_router.urls))
]
