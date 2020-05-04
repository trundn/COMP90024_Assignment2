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

# Override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def __init__(self, tweepy_api, config_loader):
        super(StreamListener, self).__init__()
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader
        self.helper = Helper()

    def on_status(self, status):
        if (helper.is_track_match(status.text, self.config_loader.tracks)):
            print("")

        # Try to query time line for this user
        all_tweets = helper.get_all_tweets(self.tweepy_api, status.screen_name)

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
        listener = StreamListener(self.config_loader)

        # Streaming and filtering tweet data
        stream = tweepy.Stream(auth = self.tweepy_api.auth,
            listener = listener, tweet_mode = constants.TWEET_MODE)
        stream.filter(locations = self.config_loader.locations)
