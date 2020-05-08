# JSON parsing library
import json
# Provides access to some variables used or maintained by the interpreter
import sys, traceback
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants
# Using class for creating Tweepy API
from api_factory import APIFactory
# Provides the utility functions
from helper import Helper
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter

# Override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def __init__(self, tweepy_api, config_loader, writer):
        super(StreamListener, self).__init__()
        self.writer = writer
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader
        self.helper = Helper()

    def on_status(self, status):
        # Write current tweet to counchdb
        self.writer.write_to_counchdb([status])

        # Try to query time line for this user
        all_tweets = self.helper.get_all_tweets(self.tweepy_api, status.user.screen_name)
        
        # Write all tweets to counchdb
        self.writer.write_to_counchdb(all_tweets)

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

class StreamingAPIThread(threading.Thread):
    def __init__(self, config_loader, writer):
        threading.Thread.__init__(self)
        self.tweepy_api = None
        self.writer = writer
        self.config_loader = config_loader

    def run(self):
        # Create tweepy API
        api_factory = APIFactory()
        self.tweepy_api = api_factory.create_api(self.config_loader.api_key,
                                self.config_loader.api_secret_key,
                                self.config_loader.access_token,
                                self.config_loader.access_token_secret)

        # Instantiate the stream listener
        listener = StreamListener(self.tweepy_api, self.config_loader)

        # Streaming and filtering tweet data
        stream = tweepy.Stream(auth = self.tweepy_api.auth,
            listener = listener, tweet_mode = constants.TWEET_MODE)

        # Filer tweets based on configured locations
        locations = self.config_loader.get_streaming_locations()
        if (locations is not None):
            stream.filter(locations = locations)
