# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Utility for creating tweepy API
import api_factory
# Utility for loading the configuration files
import config_loader

# Definition of Constants
TWEET_COUNT_PER_REQ = 200;

class SearchingAPIThread(threading.Thread):
    def __init__(self, authen_config_path, filter_config_path):
        threading.Thread.__init__(self)
        self.authen_config_path = authen_config_path
        self.filter_config_path = filter_config_path

    def run(self):
        # Load the tweet filter configuration file
        track, locations, users, languages = config_loader.load_filter_config(
            self.filter_config_path)

        # Create tweepy API
        api = api_factory.create_api(self.authen_config_path)

        while(True):
            for user_id in users:
                results  = api.user_timeline(user_id, count = TWEET_COUNT_PER_REQ)
                for tweet in results:
                    print(tweet._json)