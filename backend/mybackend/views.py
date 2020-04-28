from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Article
from .serializers import ArticleSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class TwitterViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([1, 2, 3, 4, 5])

    def retrieve(self, request, pk=None):
        return Response({"id": 1, "text": "tweeter"})
