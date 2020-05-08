# Provides the utility functions
from helper import Helper
# Provide a common protocol for objects that wish to execute code while they are active
from runnable import Runnable
# Supplies classes for manipulating dates and times
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

            if (self.helper.is_track_match(full_text.lower(), self.config_loader.track)):
                source, coordinates = self.helper.extract_coordinates(tweet)

                if (coordinates):
                    emotions = self.helper.extract_emotions(full_text)
                    word_count, pronoun_count = self.helper.extract_word_count(full_text)

                    converted_datetime = ""
                    if tweet.created_at != None:
                        converted_datetime = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S%z')

                    filter_data = {'_id' : tweet.id_str, 'created_at' : converted_datetime,\
                                'text' : full_text, 'user' : tweet.user.screen_name, \
                                'calculated_coordinates' : coordinates, \
                                'coordinates_source' : source, 'emotions': emotions, \
                                'tweet_wordcount' : word_count, "pronoun_count" : pronoun_count,\
                                'raw_data' : tweet._json}
                    
                    print(f"{tweet.id_str}    {emotions}    {word_count}    {pronoun_count}")
                    self.db_connection.write_tweet(filter_data)
