# Import module sys to get the type of exception
import sys
# Provides a standard interface to extract, format and print stack traces 
import traceback
# Provides the utility functions
from helper import Helper
# Provide a common protocol for objects that wish to execute code while they are active
from runnable import Runnable
# Supplies classes for manipulating dates and times
from datetime import datetime

class WriterJob(Runnable):
    def __init__(self, all_tweets, db_connection, config_loader, ignore_coordinates_filter = False):
        self.all_tweets = all_tweets
        self.db_connection = db_connection
        self.config_loader = config_loader
        self.ignore_coordinates_filter = ignore_coordinates_filter
        self.helper = Helper()

    def run(self):
        for tweet in self.all_tweets:
            try:
                # Extract full text
                full_text = self.helper.extract_full_text(tweet)

                if (self.helper.is_match(full_text.lower(), self.config_loader.track)):
                    source, coordinates = self.helper.extract_coordinates(tweet)
                    
                    politician_type = self.config_loader.get_politician_type(tweet.user.screen_name)
                    is_politician = (politician_type is not None) and (politician_type != "")

                    if (coordinates or (self.ignore_coordinates_filter is True) \
                                    or is_politician):
                        inside_polygon = True
                        if ((self.ignore_coordinates_filter is False) and (is_politician is False)):
                            inside_polygon = self.config_loader.within_geometry_filters(coordinates)

                        if (inside_polygon is True):
                            emotions = self.helper.extract_emotions(full_text)
                            word_count, pronoun_count = self.helper.extract_word_count(full_text)

                            converted_datetime = ""
                            if tweet.created_at != None:
                                converted_datetime = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S%z')

                            filter_data = {'_id' : tweet.id_str, 'created_at' : converted_datetime,\
                                        'text' : full_text, 'user' : tweet.user.screen_name, \
                                        'politician' : politician_type, 'calculated_coordinates' : coordinates, \
                                        'coordinates_source' : source, 'emotions': emotions, \
                                        'tweet_wordcount' : word_count, "pronoun_count" : pronoun_count,\
                                        'raw_data' : tweet._json}
                            
                            print(f"{tweet.id_str}    {emotions}    {word_count}    {pronoun_count}")
                            self.db_connection.write_tweet(filter_data)
            except:
                print("Exception", sys.exc_info()[0], "occurred.")
                traceback.print_exc(file = sys.stdout)
