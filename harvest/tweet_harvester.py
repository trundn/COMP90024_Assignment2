# Using library for system dependent functionalities
import os
# Library for command line argument parsing
import sys, getopt
# Thread for performing tweepy streaming API
from tweepy_streaming import StreamingAPIThread
# Thread for performing tweepy searching API
from tweepy_searching import SearchingAPIThread

CMD_LINE_DEFINED_ARGUMENTS = "ha:f:"
HELP_ARGUMENT = "-h"
AUTHEN_CONFIG_ARGUMENT = "-a"
FILTER_CONFIG_ARGUMENT = "-f"

def print_usage():
  print ('Usage is: tweet_harvester.py -a <the authentication configuration file> -f <the tweet filter configuration file>')

def parse_arguments(argv):
    # Initialise local variables
    authen_config_path = ""
    filter_config_path = ""

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(argv, CMD_LINE_DEFINED_ARGUMENTS)
    except getopt.GetoptError as error:
        print("Failed to parse comand line arguments. Error: %s" %error)
        print_usage()
        sys.exit(2)
        
    # Extract argument values
    for opt, arg in opts:
        if opt == HELP_ARGUMENT:
            print_usage()
            sys.exit()
        if opt in (AUTHEN_CONFIG_ARGUMENT):
            authen_config_path = arg
        elif opt in (FILTER_CONFIG_ARGUMENT):
            filter_config_path = arg

    # Return all arguments
    return authen_config_path, filter_config_path

def main(args):
    # Parse command line arguments to get the authentication and filter configuration files
    authen_config_path, filter_config_path = parse_arguments(args)

    # Start tweeter streaming API thread
    streaming = StreamingAPIThread(authen_config_path, filter_config_path)
    streaming.start()

    # Start tweeter searching API thread
    searching = SearchingAPIThread(authen_config_path, filter_config_path)
    searching.start()

# Run the actual program
if __name__ == "__main__":
    main(sys.argv[1:])
