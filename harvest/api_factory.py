# Using library for system dependent functionalities
import os
# Provides access to some variables used or maintained by the interpreter
import sys
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# Utility for loading the configuration files
import config_loader

def create_api(authen_config_path):
    # Load the authentication keys
    api_key, api_secret_key, access_token, access_token_secret = config_loader.load_authentication_config(authen_config_path)
    
    # Creating the authentication object
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
   
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret)
    
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)

    if (not api):
        print("Can't Authenticate.")
        sys.exit(-1)

    return api