from couchdb import Server

from django.conf import settings


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

    def get_tweets_per_hour(self):
        response = self.twitter_database.list('_design/tweets-per-hour', '_view/tweets-per-hour',
                                              **{'reduce': True, 'group': True})
        return response[1]

    def get_language_statistics(self):
        response = self.twitter_database.list('_design/language', '_view/language',
                                              **{'reduce': True, 'group': True})
        return response[1]
