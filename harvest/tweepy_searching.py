# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# Provides various time-related functions
import time
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants
# Provides the utility functions
from helper import Helper

class SearchingAPIThread(threading.Thread):
    def __init__(self, tweepy_api, config_loader):
        threading.Thread.__init__(self)
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader

    def run(self):
        helper = Helper()

        # Query time line for all configured users
        for user_id in self.config_loader.users:
            # Get all posible user tweets (max: 3200 tweets for each uer)
            all_tweets = helper.get_all_tweets(self.tweepy_api, user_id)
            # Sleep 2 seconds
            time.sleep(constants.TWO_SECONDS)

        # Query time line for all followers
        for user_id in self.config_loader.users:
            for follower in helper.get_followers(self.tweepy_api, user_id):
                if (constants.AUSTRALIA_COUNTRY_NAME in follower.location.lower()):
                    all_followers_tweets = helper.get_all_tweets(self.tweepy_api, follower.screen_name)
                    for tweet in all_followers_tweets:
                        print(tweet.text)