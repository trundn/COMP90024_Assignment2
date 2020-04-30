from couchdb import Server

from django.conf import settings


class TwitterDAO:
    def __init__(self):
        server_url = settings.COUCH_SERVER_URL
        database_name = settings.COUCH_DATABASE_NAME
        couch = Server(server_url)
        try:
            self.twitter_database = couch[database_name]
        except Exception:
            self.twitter_database = couch.create(database_name)

    def list(self):
        response = self.twitter_database.list('_design/top-10-tweet', '_view/top-10-tweet')
        return response[1]

    def create(self, doc):
        return self.twitter_database.save(doc)

    def retrieve(self, id):
        return self.twitter_database.get(id=id)
