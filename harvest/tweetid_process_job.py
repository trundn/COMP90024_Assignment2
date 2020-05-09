# Provides various time-related functions
import time
# Import module sys to get the type of exception
import sys
# Using library for system dependent functionalities
import os
# Provides a standard interface to extract, format and print stack traces 
import traceback
# Data manipulation tool.
import pandas as pd
# Provide a common protocol for objects that wish to execute code while they are active
from runnable import Runnable
# Provides the utility functions
from helper import Helper
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter
# The harvest constant definitions
import constants

class TweetIdProcessJob(Runnable):
    def __init__(self, tweepy_api, config_loader, writer, dataset_folder):
        self.tweepy_api = tweepy_api
        self.config_loader = config_loader
        self.writer = writer
        self.dataset_folder = dataset_folder
        self.helper = Helper()

    def lookup_tweets(self, tweet_ids):
        tweet_count = len(tweet_ids)

        try:
            for i in range((tweet_count // 100) + 1):
                all_tweets = []
                # Catch the last group if it is less than 100 tweets
                last_index = min((i + 1) * 100, tweet_count)
                # Sleep 2 seconds to avoid rate limit issue
                time.sleep(constants.TWO_SECONDS)
                full_tweets = self.tweepy_api.statuses_lookup(tweet_ids[i * 100 : last_index])
                
                # Check if tweet is in configured user filter locations
                for tweet in full_tweets:
                    if (hasattr(tweet, constants.PLACE) \
                        and tweet.place is not None \
                        and tweet.place.country is not None):

                        location = tweet.place.country.lower()
                        if (constants.AUSTRALIA_COUNTRY_NAME == location):
                            all_tweets.append(tweet)
                    else:
                        location = tweet.user.location.lower()
                        if (self.helper.is_match(location, self.config_loader.user_location_filters)):
                            all_tweets.append(tweet)

                # Write all tweets to counchdb
                if (all_tweets):
                    self.writer.write_to_counchdb(all_tweets)

            return full_tweets
        except:
            print("Failed to loopkup statuses.")
            traceback.print_exc(file = sys.stdout)

    def run(self):
        try:
            filenames = os.listdir(self.dataset_folder)
            for filename in filenames:
                data_frame = None

                data_path = os.path.join(self.dataset_folder, filename)
                if os.path.exists(data_path):
                    data_frame = pd.read_csv(data_path, delimiter = constants.TAB_CHAR)
                    self.lookup_tweets(data_frame[constants.TWEET_ID_COLUMN].values.tolist())
                else:
                    print("The data set of tweetid does not exist. Path: %s", data_path)
        except:
            print("Exception", sys.exc_info()[0], "occurred.")
            traceback.print_exc(file = sys.stdout)