from couchdb import Server


class TwitterDAO:
    couch = Server('http://admin:admin@localhost:5984')
    tweetdb = couch['tweet']

    def get_all_tweets(self):
        response = self.tweetdb.list('_design/top-10-tweet', '_view/top-10-tweet')
        return response[1]
