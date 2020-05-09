# Provides various time-related functions
import time
# Message Passing Interface (MPI) standard library
from mpi4py import MPI
# Using library for system dependent functionalities
import os
# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Using class for creating Tweepy API
from api_factory import APIFactory
# Uility to write tweet data to CounchDB
from tweet_writer import TweetWriter
# Responsible for processing tweet id dataset
from tweetid_process_job import TweetIdProcessJob
# The harvest constant definitions
import constants

class TweetIdQueryThread(threading.Thread):
    def __init__(self, config_loader, writer, threadpool_job_executor):
        threading.Thread.__init__(self)
        self.writer = writer
        self.tweepy_api = None
        self.config_loader = config_loader
        self.threadpool_job_executor = threadpool_job_executor

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
            job = TweetIdProcessJob(self.tweepy_api, self.config_loader, self.writer, folder)
            self.threadpool_job_executor.queue(job)

        while(self.threadpool_job_executor.is_any_thread_alive() is True):
             # Sleep 1 second before checking thread alive status again
            time.sleep(constants.ONE_SECOND)

