# JSON parsing library
import json
# Provides access to some variables used or maintained by the interpreter
import sys
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants
# Provides the utility functions
from helper import Helper
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter

# Override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def __init__(self, tweepy_api, config_loader):
        super(StreamListener, self).__init__()
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader
        self.helper = Helper()
        self.writer = TweetWriter()

    def on_status(self, status):
        # Write current tweet to counchdb
        self.writer.write_to_counchdb([status])

        # Try to query time line for this user
        all_tweets = helper.get_all_tweets(self.tweepy_api, status.screen_name)
        
        # Write all tweets to counchdb
        self.writer.write_to_counchdb(all_tweets)

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

class StreamingAPIThread(threading.Thread):
    def __init__(self, tweepy_api, config_loader):
        threading.Thread.__init__(self)
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader

    def run(self):
        # Instantiate the stream listener
        listener = StreamListener(self.tweepy_api, self.config_loader)

        # Streaming and filtering tweet data
        stream = tweepy.Stream(auth = self.tweepy_api.auth,
            listener = listener, tweet_mode = constants.TWEET_MODE)
        stream.filter(locations = self.config_loader.locations)
