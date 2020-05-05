# Library for working with CouchDB
import couchdb
# The harvest constant definitions
import harvest.constants

class CouchDBConnection(object):
    def __init__(self, connection_string, lock):
        self.lock = lock
        self.connection_string = connection_string
        self.server = couchdb.Server(self.connection_string)

    def init_database(self):
        if harvest.constants.TWEETS_DATABASE in self.server:
            self.database = self.server[harvest.constants.TWEETS_DATABASE]
        else:
            self.database = self.server.create(harvest.constants.TWEETS_DATABASE)

    def write_tweet(self, tweet_content):
        if ((tweet_content is not None) and isinstance(tweet_content, dict)):
            tweet_id = tweet_content['_id']
            with self.lock:
                if ((tweet_id is not None) and (tweet_id not in self.database)):
                    self.database.save(tweet_content)