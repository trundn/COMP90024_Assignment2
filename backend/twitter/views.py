from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import views
from .daos import TwitterDAO, StatisticsDAO, SentimentMapDAO, UserDAO, MovementDAO
from .models import Polygon
from .serializers import PolygonSerializer, PartialPolygonSerializer
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


class PolygonViewSet(viewsets.ModelViewSet):
    serializer_class = PolygonSerializer
    queryset = Polygon.objects.all()

    def list(self, request, *args, **kwargs):
        polygons = Polygon.objects.all()
        serializer = PartialPolygonSerializer(polygons, many=True)
        return Response(serializer.data)


class TweetsPerHourView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_tweets_per_hour()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TotalTweetsByDayAndHour(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_total_tweets_by_day_and_hour()
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
    sentiment_map_dao = SentimentMapDAO()

    def get(self, request):
        try:
            bottom_left_point = request.query_params.get('bottom_left_point')
            top_right_point = request.query_params.get('top_right_point')
            # bottom_left_point = [-45, 110]
            # top_right_point = [-8, 155]
            result = self.sentiment_map_dao.get_tweets_in_rectangle(bottom_left_point, top_right_point)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsInPolygonView(views.APIView):
    map_dao = SentimentMapDAO()

    def post(self, request):
        try:
            polygons = request.data
            result = self.map_dao.get_tweets_in_polygon(polygons)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class StatisticsInPolygonView(views.APIView):
    map_dao = SentimentMapDAO()

    def get(self, request, pk):
        result = []
        data = Polygon.objects.get(pk=pk)
        serializer = PolygonSerializer(data)
        data = serializer.data
        content = json.loads(data['content'])
        features = content['features']
        for feature in features:
            feature_code = feature['properties']['feature_code']
            feature_name = feature['properties']['feature_name']
            polygon_data = feature['geometry']['coordinates']
            result.append({
                'code': feature_code,
                'name': feature_name,
                'statistics': self.map_dao.get_statistics_in_polygon(polygon_data)
            })
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            polygons = request.data
            result = self.map_dao.get_statistics_in_polygon(polygons)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FeelingsAboutCovid(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            about_covid = request.query_params.get('about_covid')
            result = self.statistics_dao.get_feelings_about_covid(str(about_covid))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovementView(views.APIView):
    movement_dao = MovementDAO()

    def get(self, request):
        try:
            limit = request.query_params.get('limit')
            if limit is not None:
                limit = int(limit)
            result = self.movement_dao.get_movement_data(limit)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FindRouteView(views.APIView):
    movement_dao = MovementDAO()

    def get(self, request):
        try:
            user_key = request.query_params.get('user_key')
            user_key = json.loads(user_key)
            result = self.movement_dao.get_route_by_user(user_key)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetMostActiveUsersView(views.APIView):
    movement_dao = MovementDAO()

    def get(self, request):
        try:
            result = self.movement_dao.get_most_active_users()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetUserInfoView(views.APIView):
    user_dao = UserDAO()

    def get(self, request, pk):
        try:
            result = self.user_dao.get_user_info(int(pk))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsByCategoriesView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.tweets_by_categories()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsWithCoordinatesView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_tweets_with_coordinates()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsWithEmoValuesAndProCntView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            skip = request.query_params.get('skip')
            limit = request.query_params.get('limit')
            if skip is not None:
                skip = int(skip)
            else:
                skip = 0
            if limit is not None:
                limit = int(limit)
            result = self.statistics_dao.get_tweets_with_emo_and_procnt(skip, limit)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsByPoliticalPartiesView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_tweets_by_political_parties()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsByPoliticiansView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_tweets_by_politicians()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MostPositiveHoursView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_most_positive_hours()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class MostNegativeHoursView(views.APIView):
    statistics_dao = StatisticsDAO()

    def get(self, request):
        try:
            result = self.statistics_dao.get_most_negative_hours()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
