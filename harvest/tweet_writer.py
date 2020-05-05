# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# Provides the utility functions
from harvest.helper import Helper
# Utility for working with CouchDB
from harvest.couchdb_connection import CouchDBConnection
from harvest.job_executor import JobExecutor
from harvest.writer_job import WriterJob

class TweetWriter(object):
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.lock = threading.Lock()
        self.database_connection = CouchDBConnection(
            self.config_loader.couchdb_connection_string, self.lock)
        self.threadpool_job_executor = JobExecutor(-1, 50, 50000)

    def write_to_counchdb(self, all_tweets):
        if (all_tweets is not None):
            job = WriterJob(all_tweets, self.database_connection)
            self.threadpool_job_executor.queue(job)
