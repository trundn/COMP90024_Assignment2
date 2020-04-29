# JSON parsing library
import json
# Provides access to some variables used or maintained by the interpreter
import sys
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants;

# Override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status._json)

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
        listener = StreamListener()

        # Streaming and filtering tweet data
        stream = tweepy.Stream(auth = self.tweepy_api.auth,
            listener = listener, tweet_mode = constants.TWEET_MODE)
        stream.filter(track = self.config_loader.track,
            locations = self.config_loader.locations, languages = self.config_loader.languages)