from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import views
from .daos import TwitterDAO, StatisticsDAO, MapDAO, RouteDAO, UserDAO, HomeDAO
from .models import Polygon
from .serializers import PolygonSerializer
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


class FindRouteView(views.APIView):
    route_dao = RouteDAO()

    def get(self, request):
        try:
            user_key = request.query_params.get('user_key')
            user_key = json.loads(user_key)
            result = self.route_dao.get_route_by_user(user_key)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetMostActiveUsersView(views.APIView):
    route_dao = RouteDAO()

    def get(self, request):
        try:
            result = self.route_dao.get_most_active_users()
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
    home_dao = HomeDAO()

    def get(self, request):
        try:
            result = self.home_dao.tweets_by_categories()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TweetsWithCoordinatesView(views.APIView):
    home_dao = HomeDAO()

    def get(self, request):
        try:
            result = self.home_dao.tweets_with_coordinates()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
