# Using library for system dependent functionalities
import os
# Library for command line argument parsing
import sys, getopt
# Using class for loading all needed configurations
from config_loader import ConfigurationLoader
# Using class for creating Tweepy API
from api_factory import APIFactory;
# Thread for performing tweepy streaming API
from tweepy_streaming import StreamingAPIThread
# Thread for performing tweepy searching API
from tweepy_searching import SearchingAPIThread
# The harvest constant definitions
import constants;

def print_usage():
  print ('Usage is: tweet_harvester.py -a <the authentication configuration file> -f <the tweet filter configuration file>')

def parse_arguments(argv):
    # Initialise local variables
    authen_config_path = ""
    filter_config_path = ""

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(argv, constants.CMD_LINE_DEFINED_ARGUMENTS)
    except getopt.GetoptError as error:
        print("Failed to parse comand line arguments. Error: %s" %error)
        print_usage()
        sys.exit(2)
        
    # Extract argument values
    for opt, arg in opts:
        if opt == constants.HELP_ARGUMENT:
            print_usage()
            sys.exit()
        if opt in (constants.AUTHEN_CONFIG_ARGUMENT):
            authen_config_path = arg
        elif opt in (constants.FILTER_CONFIG_ARGUMENT):
            filter_config_path = arg

    # Return all arguments
    return authen_config_path, filter_config_path

def main(args):
    # Parse command line arguments to get the authentication and filter configuration files
    authen_config_path, filter_config_path = parse_arguments(args)

    # Instantiate the configuration loader
    config_loader = ConfigurationLoader(authen_config_path, filter_config_path)
    config_loader.load_authentication_config()
    config_loader.load_filter_config()

    # Create tweepy API
    api_factory = APIFactory(config_loader)
    tweepy_api = api_factory.create_api()

    # Start tweeter streaming API thread
    streaming = StreamingAPIThread(tweepy_api, config_loader)
    streaming.start()

    # Start tweeter searching API thread
    searching = SearchingAPIThread(tweepy_api, config_loader)
    searching.start()

# Run the actual program
if __name__ == "__main__":
    main(sys.argv[1:])
