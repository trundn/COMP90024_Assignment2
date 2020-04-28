from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from .daos import TwitterDAO


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class TwitterViewSet(viewsets.ViewSet):
    twitterDAO = TwitterDAO()

    def list(self, request):
        all_tweets = self.twitterDAO.get_all_tweets()
        return Response(all_tweets)

    def post(self, request):
        return True

    def retrieve(self, request, pk=None):
        return True
