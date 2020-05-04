# Provides the utility functions
from helper import Helper

class TweetWriter(object):
    def write_to_counchdb(self, all_tweets, config_loader):
        if (all_tweets is not None):
            helper = Helper()

            for tweet in all_tweets:
                if (helper.is_track_match(tweet.text, config_loader.tracks)):
                    source, coordinates = helper.extract_coordinates(tweet)

                    if (coordinates is not None):

                        filter_data = {'_id' : tweet.id_str, 'created_at' : tweet.created_at,\
                                'text' : tweet.text, 'user' : tweet.user, 'geo' : tweet.geo,\
                                'coordinates' : tweet.coordinates, 'place' : tweet.place,\
                                'calculated_coordinates' : coordinates, 'coordinates_source' : source,\
                                'raw_data' : tweet._json}
