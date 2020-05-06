# Provides the utility functions
from harvest.helper import Helper
# Provide a common protocol for objects that wish to execute code while they are active
from harvest.runnable import Runnable

class WriterJob(Runnable):
    def __init__(self, all_tweets, db_connection):
        self.all_tweets = all_tweets
        self.db_connection = db_connection

    def run(self):
        helper = Helper()

        for tweet in self.all_tweets:
            
            # Extract full text
            if (tweet["doc"]["truncated"] == True):
                tweet_text = data_json["doc"]["extended_tweet"]["full_text"]
            else:
                tweet_text = data_json["doc"]["text"]

            if (helper.is_track_match(tweet_text, self.config_loader.tracks)):
                source, coordinates = helper.extract_coordinates(tweet)
                emotions = helper.extract_emotions(tweet_text)                

                if (coordinates is not None):
                    filter_data = {'_id' : tweet.id_str, 'created_at' : tweet.created_at,\
                                'text' : tweet_text, 'user' : tweet.user, 'geo' : tweet.geo,\
                                'coordinates' : tweet.coordinates, 'place' : tweet.place,\
                                'calculated_coordinates' : coordinates, 'coordinates_source' : source,\
                                'emotions': emotions, 'raw_data' : tweet._json}
                    self.db_connection.write_tweet(filter_data)
