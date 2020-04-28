# JSON parsing library
import json
# Using library for system dependent functionalities
import os

# Definition of Constants
JSON_API_KEY_PROP = "api_key"
JSON_API_SECRET_KEY_PROP = "api_secret_key"
JSON_ACCESS_TOKEN_PROP = "access_token"
JSON_ACCESS_TOKEN_SECRET = "access_token_secret"

JSON_LOCATIONS_PROP = "locations"
JSON_LANGUAGES_PROP = "languages"
JSON_TRACK_PROP = "track"
JSON_USERS_PROP = "users"

def load_authentication_config(file_path):
    api_key = ""
    api_secret_key = ""
    access_token = ""
    access_token_secret = ""

    if os.path.exists(file_path):
        with open(file_path) as fstream:
            try:
                config_content = json.loads(fstream.read())
                api_key = config_content[JSON_API_KEY_PROP]
                api_secret_key = config_content[JSON_API_SECRET_KEY_PROP]
                access_token = config_content[JSON_ACCESS_TOKEN_PROP]
                access_token_secret = config_content[JSON_ACCESS_TOKEN_SECRET]
            except Exception as exception:
                print("Error occurred during loading the authentication configuration file. Exception: %s" %exception)
    else:
        print("The authentication configuration file does not exist. Path: %s", file_path)

    return api_key, api_secret_key, access_token, access_token_secret

def load_filter_config(file_path):
        locations = []
        languages = []
        track = []
        users = []

        if os.path.exists(file_path):
            with open(file_path) as fstream:
                try:
                    config_content = json.loads(fstream.read())
                    track = config_content[JSON_TRACK_PROP]
                    locations = config_content[JSON_LOCATIONS_PROP]
                    users = config_content[JSON_USERS_PROP]
                    languages = config_content[JSON_LANGUAGES_PROP]
                except Exception as exception:
                    print("Error occurred during loading the tweet filter configuration file. Exception: %s" %exception)
        else:
            print("The authentication configuration file does not exist. Path: %s", file_path)

        return track, locations, users, languages
