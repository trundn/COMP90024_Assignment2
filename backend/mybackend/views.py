from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from couchdb import Server


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class TwitterViewSet(viewsets.ViewSet):
    couch = Server('http://admin:admin@localhost:5984')
    tweetdb = couch['tweet']

    def list(self, request):
        response = self.tweetdb.list('_design/top-10-tweet', '_view/top-10-tweet')
        return Response(response[1])

    def post(self, request):
        return True

    def retrieve(self, request, pk=None):
        return True
