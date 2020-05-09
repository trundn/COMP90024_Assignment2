# Message Passing Interface (MPI) standard library
from mpi4py import MPI
# Provides various time-related functions
import time
# Using library for system dependent functionalities
import os
# Import module sys to get the type of exception
import sys
# Provides a standard interface to extract, format and print stack traces 
import traceback
# Data manipulation tool.
import pandas as pd
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Using class for creating Tweepy API
from api_factory import APIFactory
# Provides the utility functions
from helper import Helper
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter
# The harvest constant definitions
import constants

class TweetIdQueryThread(threading.Thread):
    def __init__(self, config_loader, writer):
        threading.Thread.__init__(self)
        self.writer = writer
        self.tweepy_api = None
        self.config_loader = config_loader
        self.helper = Helper()

    def lookup_tweets(self, tweet_ids):
        tweet_count = len(tweet_ids)

        try:
            for i in range((tweet_count // 100) + 1):
                all_tweets = []
                # Catch the last group if it is less than 100 tweets
                last_index = min((i + 1) * 100, tweet_count)
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
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        processor_size = comm.Get_size()

        dataset_folders = self.config_loader.get_tweeid_dataset(rank, processor_size)
        api_key, api_secret_key, access_token, access_token_secret = self.config_loader.get_searching_authen(rank)

        api_factory = APIFactory()
        self.tweepy_api = api_factory.create_api(api_key, api_secret_key,
                                access_token, access_token_secret)

        for folder in dataset_folders:
            print(f"Processing tweetid data set folder [{folder}]")
            all_filenames = os.listdir(folder)

            try:
                for filename in all_filenames:
                    data_frame = None

                    data_path = os.path.join(folder, filename)
                    if os.path.exists(data_path):
                        data_frame = pd.read_csv(data_path, delimiter = constants.TAB_CHAR)
                        self.lookup_tweets(data_frame[constants.TWEET_ID_COLUMN].values.tolist())
                    else:
                        print("The data set of tweetid does not exist. Path: %s", data_path)
            except:
                print("Exception", sys.exc_info()[0], "occurred.")

        print("Finished processing tweetid dataset.")


