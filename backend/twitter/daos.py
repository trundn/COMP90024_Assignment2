from couchdb import Server

from django.conf import settings

from shapely.geometry import Point
from shapely.geometry import Polygon, MultiPolygon


class DAO:
    def __init__(self):
        server_url = settings.COUCH_SERVER_URL
        database_name = settings.COUCH_DATABASE_NAME
        couch = Server(server_url)
        try:
            self.twitter_database = couch[database_name]
        except Exception:
            self.twitter_database = couch.create(database_name)


class TwitterDAO(DAO):
    def __init__(self):
        super().__init__()

    def list(self):
        response = self.twitter_database.list('_design/top-10-tweet', '_view/top-10-tweet')
        return response[1]

    def create(self, doc):
        return self.twitter_database.save(doc)

    def retrieve(self, document_id):
        return self.twitter_database.get(id=document_id)


class StatisticsDAO(DAO):
    def __init__(self):
        super().__init__()

    def tweets_by_categories(self):
        params = {
            'reduce': True,
            'group': True
        }
        response = self.twitter_database.list('_design/statistics', '_view/tweets-by-categories', **params)
        rows = response[1]["rows"]
        return rows

    def tweets_with_coordinates(self):
        params = {
            'reduce': True,
            'group_level': 2
        }
        response = self.twitter_database.list('_design/statistics', '_view/tweets-with-coordinates', **params)
        rows = response[1]["rows"]
        return rows

    def get_tweets_per_hour(self):
        params = {'inclusive': True, 'reduce': True, 'group': True}
        response = self.twitter_database.list('_design/statistics', '_view/tweets-per-hour', **params)
        return response[1]

    def get_total_tweets_by_day_and_hour(self):
        params = {'reduce': True, 'group_level': 2}
        response = self.twitter_database.list('_design/statistics', '_view/total-tweets-by-day-n-hour', **params)
        rows = response[1]["rows"]
        return rows

    def get_language_statistics(self):
        params = {'inclusive': True, 'reduce': True, 'group': True}
        response = self.twitter_database.list('_design/statistics', '_view/language', **params)
        return response[1]

    def get_tweets_with_emo_and_procnt(self, skip, limit):
        params = {
            'skip': skip
        }
        if (limit is not None):
            params['limit'] = limit
        response = self.twitter_database.list('_design/statistics', '_view/tweets-with-emo-val-and-pro-cnt', **params)
        rows = response[1]["rows"]
        return rows


class SentimentMapDAO(DAO):
    def __init__(self):
        super().__init__()

    def get_tweets_in_rectangle(self, bottom_left_point, top_right_point):
        params = {
            'inclusive_end': True,
            'start_key': bottom_left_point,
            'end_key': top_right_point
        }
        try:
            response = self.twitter_database.list('_design/sentiment-map', '_view/within-polygon', **params)
            tweets = response[1]["rows"]
        except Exception as e:
            tweets = []
        return tweets

    def get_tweets_in_polygon(self, polygon_data):
        tweets_in_polygon = []

        for polygon_data_item in polygon_data:
            polygon = Polygon(polygon_data_item[0])
            bottom_left_point = [polygon.bounds[0], polygon.bounds[1]]
            top_right_point = [polygon.bounds[2], polygon.bounds[3]]
            tweets = self.get_tweets_in_rectangle(bottom_left_point, top_right_point)
            for tweet in tweets:
                if polygon.contains(Point(tweet['key'])):
                    tweets_in_polygon.append(tweet)

        return tweets_in_polygon

    def get_statistics_in_polygon(self, polygon_data):
        statistics = {
            "number_of_positive_tweets": 0,
            "number_of_neural_tweets": 0,
            "number_of_negative_tweets": 0
        }
        tweets_in_polygon = self.get_tweets_in_polygon(polygon_data)
        for tweet in tweets_in_polygon:
            if tweet['value'] == 'POSITIVE':
                statistics['number_of_positive_tweets'] = statistics['number_of_positive_tweets'] + 1
            elif tweet['value'] == 'NEUTRAL':
                statistics['number_of_neural_tweets'] = statistics['number_of_neural_tweets'] + 1
            elif tweet['value'] == 'NEGATIVE':
                statistics['number_of_negative_tweets'] = statistics['number_of_negative_tweets'] + 1

        return statistics


class UserDAO(DAO):
    def get_user_info(self, pk):
        result = []

        params = {
            'limit': 1,
            'key': pk
        }
        response = self.twitter_database.list('_design/user', '_view/user', **params)
        rows = response[1]["rows"]
        if (len(rows) > 0):
            return rows[0]
        else:
            return None


class MovementDAO(DAO):
    def get_movement_data(self):
        params = {
            'reduce': True,
            'group': True
        }
        response = self.twitter_database.list('_design/movement', '_view/movement', **params)
        rows = response[1]["rows"]
        return rows

    def get_route_by_user(self, user_key):
        print(user_key)
        result = []

        params = {
            'reduce': False,
            'key': user_key
        }
        response = self.twitter_database.list('_design/movement', '_view/find-route', **params)
        rows = response[1]["rows"]
        sorted_rows = sorted(rows, key=lambda i: i['value'][1])
        for row in sorted_rows:
            result.append(row['value'][0])

        return result

    def get_most_active_users(self):
        result = []

        params = {
            'limit': 500,
            'reduce': True,
            'group': True
        }
        response = self.twitter_database.list('_design/movement', '_view/find-route', **params)
        rows = response[1]["rows"]
        sorted_rows = sorted(rows, key=lambda i: i['value'], reverse=True)

        return sorted_rows
