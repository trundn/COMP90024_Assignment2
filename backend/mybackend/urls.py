from django.urls import path, include
from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ArticleViewSet, basename='article')

urlpatterns = [
    path('article/', include(router.urls))
]
