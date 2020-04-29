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

class ConfigurationLoader(object):
    def __init__(self, authen_config_path, filter_config_path):
        self.authen_config_path = authen_config_path
        self.filter_config_path = filter_config_path

        self.api_key = ""
        self.api_secret_key = ""
        self.access_token = ""
        self.access_token_secret = ""

        self.locations = []
        self.languages = []
        self.track = []
        self.users = []

    def load_authentication_config(self):
        if os.path.exists(self.authen_config_path):
            with open(self.authen_config_path) as fstream:
                try:
                    config_content = json.loads(fstream.read())
                    self.api_key = config_content[JSON_API_KEY_PROP]
                    self.api_secret_key = config_content[JSON_API_SECRET_KEY_PROP]
                    self.access_token = config_content[JSON_ACCESS_TOKEN_PROP]
                    self.access_token_secret = config_content[JSON_ACCESS_TOKEN_SECRET]
                except Exception as exception:
                    print("Error occurred during loading the authentication configuration file. Exception: %s" %exception)
        else:
            print("The authentication configuration file does not exist. Path: %s", self.authen_config_path)

    def load_filter_config(self):
            if os.path.exists(self.filter_config_path):
                with open(self.filter_config_path) as fstream:
                    try:
                        config_content = json.loads(fstream.read())
                        self.track = config_content[JSON_TRACK_PROP]
                        self.locations = config_content[JSON_LOCATIONS_PROP]
                        self.users = config_content[JSON_USERS_PROP]
                        self.languages = config_content[JSON_LANGUAGES_PROP]
                    except Exception as exception:
                        print("Error occurred during loading the tweet filter configuration file. Exception: %s" %exception)
            else:
                print("The authentication configuration file does not exist. Path: %s", file_path)
