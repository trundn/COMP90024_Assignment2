from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import views
from .daos import TwitterDAO, StatisticsDAO, MapDAO
import json


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
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class LanguageStatisticsView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_language_statistics()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsInRectangleView(views.APIView):
    map_dao = MapDAO()

    def get(self, request):
        try:
            bottom_left_point = request.query_params.get('bottom_left_point')
            top_right_point = request.query_params.get('top_right_point')
            # bottom_left_point = [-45, 110]
            # top_right_point = [-8, 155]
            result = self.map_dao.get_tweets_in_rectangle(bottom_left_point, top_right_point)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsInPolygonView(views.APIView):
    map_dao = MapDAO()

    def post(self, request):
        try:
            polygons = request.data
            result = self.map_dao.get_tweets_in_polygon(polygons)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class StatisticsInPolygonView(views.APIView):
    map_dao = MapDAO()

    def post(self, request):
        try:
            polygons = request.data
            result = self.map_dao.get_statistics_in_polygon(polygons)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
