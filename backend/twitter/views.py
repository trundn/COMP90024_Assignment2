from rest_framework.response import Response
from rest_framework import viewsets
from .daos import TwitterDAO


class TwitterViewSet(viewsets.ViewSet):
    twitterDAO = TwitterDAO()

    def list(self, request):
        all_tweets = self.twitterDAO.list()
        return Response(all_tweets)

    def create(self, request):
        result = self.twitterDAO.create(request.data)
        return Response(result)

    def retrieve(self, request, pk=None):
        details = self.twitterDAO.retrieve(pk)
        return Response(details)

    def update(self, request, pk=None):
        return Response("Hasn't implemented!")
