# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants;

class SearchingAPIThread(threading.Thread):
    def __init__(self, tweepy_api, config_loader):
        threading.Thread.__init__(self)
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader

    def run(self):
        while(True):
            for user_id in self.config_loader.users:
                results  = self.tweepy_api.user_timeline(user_id, count = constants.TWEET_COUNT_PER_REQ)
                for tweet in results:
                    print(tweet._json)