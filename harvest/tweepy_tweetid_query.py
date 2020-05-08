# Message Passing Interface (MPI) standard library
from mpi4py import MPI
# Provides various time-related functions
import time
# Using library for system dependent functionalities
import os
# Import module sys to get the type of exception
import sys
# Data manipulation tool.
import pandas as pd
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Using class for creating Tweepy API
from api_factory import APIFactory
# The harvest constant definitions
import constants
# Provides the utility functions
from helper import Helper
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter

class TweetIdQueryThread(threading.Thread):
    def __init__(self, config_loader):
        threading.Thread.__init__(self)
        self.tweepy_api = None
        self.config_loader = config_loader
        self.helper = Helper()
        self.writer = TweetWriter(self.config_loader)

    
    def get_tweet_status(self, all_tweet_ids):
        all_tweets = []

        # Sleep 2 seconds to avoid rate limit issue
        time.sleep(constants.TWO_SECONDS)
        
        # Get tweet status from tweetid list
        historic_tweets = self.tweepy_api.get_status(all_tweet_ids, tweet_mode = constants.TWEET_MODE)
        
        # Check if tweet is in configured user filter locations
        for tweet in historic_tweets:
            if (self.helper.is_match(tweet.user.location.lower(), self.config_loader.user_location_filters)):
                print(tweet.user.location)
                all_tweets.append(tweet)

        # Write all tweets to counchdb
        if (all_tweets):
            self.writer.write_to_counchdb(all_tweets)

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
                    all_tweet_ids = []
                    data_frame = None

                    data_path = os.path.join(folder, filename)
                    if os.path.exists(data_path):
                        data_frame = pd.read_csv(data_path, delimiter = constants.TAB_CHAR)
                        for tweet_id in data_frame[constants.TWEET_ID_COLUMN]:
                            try:
                                all_tweet_ids.append(tweet_id)
                                if (len(all_tweet_ids) == constants.LIMIT_COUNT_PER_REQ):
                                    self.get_tweet_status(all_tweet_ids)
                                    all_tweet_ids = []
                            except:
                                print(f"Cannot query tweet from [{tweet_id}]")

                        if (all_tweet_ids):
                            self.get_tweet_status(all_tweet_ids)
                    else:
                        print("The data set of tweetid does not exist. Path: %s", data_path)
            except:
                print("Exception", sys.exc_info()[0], "occurred.")

        print("Finished processing tweetid dataset.")


