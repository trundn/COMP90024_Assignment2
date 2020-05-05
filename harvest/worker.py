# Constructs higher-level threading interfaces on top of the lower level _thread module
import threading
# import module sys to get the type of exception
import sys
# Useful in threaded programming when information must be exchanged safely between multiple threads
from Queue import Queue
# Provide a common protocol for objects that wish to execute code while they are active
from runnable import Runnable
# Useful in thread-safe get and set boolean value
from atomic_boolean import AtomicBoolean

class Worker(threading.Thread):
    def __init__(self, is_stopped, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.daemon = True
        self.is_stopped = is_stopped
        self.handling_job_list = []

    def run(self):
        try:
            while(not self.is_stopped.get()):
                job = self.queue.get()
                if ((job is not None) and (isinstance(job, Runnable))) :
                    runnable = Runnable(job)
                    self.handling_job_list.append(runnable)
                    runnable.run()
        except:
            print("Exception", sys.exc_info()[0], "occured.")

