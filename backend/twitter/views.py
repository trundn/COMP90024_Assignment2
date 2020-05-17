from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import views
from .daos import TwitterDAO, StatisticsDAO


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


class TweetsPerHourView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_tweets_per_hour()
            return Response(result, status=status.HTTP_200_OK)
        except Exception(e):
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class LanguageStatisticsView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_language_statistics()
            return Response(result, status=status.HTTP_200_OK)
        except Exception(e):
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
