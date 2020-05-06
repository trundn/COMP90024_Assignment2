# Provides the utility functions
from helper import Helper
# Provide a common protocol for objects that wish to execute code while they are active
from runnable import Runnable
from datetime import datetime

class WriterJob(Runnable):
    def __init__(self, all_tweets, db_connection, config_loader):
        self.all_tweets = all_tweets
        self.db_connection = db_connection
        self.config_loader = config_loader
        self.helper = Helper()

    def run(self):
        for tweet in self.all_tweets:
            # Extract full text
            full_text = self.helper.extract_full_text(tweet)

            if (self.helper.is_track_match(full_text, self.config_loader.track)):
                source, coordinates = self.helper.extract_coordinates(tweet)
                emotions = self.helper.extract_emotions(full_text)

                converted_datetime = ""
                if tweet.created_at != None:
                    converted_datetime = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S%z')
                
                if (coordinates):
                    filter_data = {'_id' : tweet.id_str, 'created_at' : converted_datetime,\
                                'text' : full_text, 'user' : tweet.user.screen_name, 'geo' : tweet.geo,\
                                'coordinates' : tweet.coordinates,\
                                'calculated_coordinates' : coordinates, 'coordinates_source' : source,\
                                'emotions': emotions, 'raw_data' : tweet._json}
                    print(filter_data)
                    self.db_connection.write_tweet(filter_data)
