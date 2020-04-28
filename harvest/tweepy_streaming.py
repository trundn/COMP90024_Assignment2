# JSON parsing library
import json
# Provides access to some variables used or maintained by the interpreter
import sys
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Utility for creating tweepy API
import api_factory
# Utility for loading the configuration files
import config_loader

# Definition of Constants
TWEET_MODE = "extended"

# Override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status._json)

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

class StreamingAPIThread(threading.Thread):
    def __init__(self, authen_config_path, filter_config_path):
        threading.Thread.__init__(self)
        self.authen_config_path = authen_config_path
        self.filter_config_path = filter_config_path

    def run(self):
        # Instantiate the stream listener
        listener = StreamListener()

        # Load the tweet filter configuration file
        track, locations, users, languages = config_loader.load_filter_config(
            self.filter_config_path)

        # Create tweepy API
        api = api_factory.create_api(self.authen_config_path)

        # Streaming and filtering tweet data
        stream = tweepy.Stream(auth = api.auth, listener = listener, tweet_mode = TWEET_MODE)
        stream.filter(track = track, locations = locations, languages = languages)