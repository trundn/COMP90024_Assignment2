# JSON parsing library
import json
# Using library for system dependent functionalities
import os
# The harvest constant definitions
import constants

class ConfigurationLoader(object):
    def __init__(self, authen_config_path, filter_config_path, database_config_path):
        self.authen_config_path = authen_config_path
        self.filter_config_path = filter_config_path
        self.database_config_path = database_config_path

        self.api_key = ""
        self.api_secret_key = ""
        self.access_token = ""
        self.access_token_secret = ""

        self.track = []
        self.users = []

        self.streaming = {}
        self.searching = {}

        self.couchdb_connection_string = ""

    def load_authentication_config(self):
        if os.path.exists(self.authen_config_path):
            with open(self.authen_config_path) as fstream:
                try:
                    config_content = json.loads(fstream.read())
                    self.api_key = config_content[constants.JSON_API_KEY_PROP]
                    self.api_secret_key = config_content[constants.JSON_API_SECRET_KEY_PROP]
                    self.access_token = config_content[constants.JSON_ACCESS_TOKEN_PROP]
                    self.access_token_secret = config_content[constants.JSON_ACCESS_TOKEN_SECRET]
                except Exception as exception:
                    print("Error occurred during loading the authentication configuration file. Exception: %s" %exception)
        else:
            print("The authentication configuration file does not exist. Path: %s", self.authen_config_path)

    def load_filter_config(self):
            if os.path.exists(self.filter_config_path):
                with open(self.filter_config_path) as fstream:
                    try:
                        config_content = json.loads(fstream.read())
                        self.streaming = config_content[constants.JSON_STREAMING_SECTION_PROP]
                        self.searching = config_content[constants.JSON_SEARCHING_SECTION_PROP]
                        self.track = config_content[constants.JSON_TRACK_PROP]
                    except Exception as exception:
                        print("Error occurred during loading the tweet filter configuration file. Exception: %s" %exception)
            else:
                print("The filter configuration file does not exist. Path: %s", self.filter_config_path)

    def load_couchdb_config(self):
        if os.path.exists(self.database_config_path):
                with open(self.database_config_path) as fstream:
                    try:
                        config_content = json.loads(fstream.read())

                        username = config_content[constants.JSON_COUCHDB_SECTION_PROP][constants.JSON_USERNAME_PROP]
                        password = config_content[constants.JSON_COUCHDB_SECTION_PROP][constants.JSON_PASSWORD_PROP]
                        host = config_content[constants.JSON_COUCHDB_SECTION_PROP][constants.JSON_HOST_PROP]
                        port = config_content[constants.JSON_COUCHDB_SECTION_PROP][constants.JSON_PORT_PROP]

                        self.couchdb_connection_string = "http://{}:{}@{}:{}/".format(username, password, host, port)
                    except Exception as exception:
                        print("Error occurred during loading the tweet database configuration file. Exception: %s" %exception)
        else:
            print("The database configuration file does not exist. Path: %s", self.database_config_path)
    
    def get_streaming_locations(self):
        locations = []

        if (self.streaming is not None):
            locations = self.streaming[constants.JSON_LOCATIONS_PROP]

        return locations

    def get_searching_users(self, processor_id):
        users = []

        if (self.searching is not None):
            politicians = self.searching[constants.JSON_POLITICIANS_PROP]
            if (politicians is not None):
                processor = politicians["processor".format(processor_id)]
                if (processor is not None):
                    users = processor[constants.JSON_USERS_PROP]

        return users

    def get_searching_authen(self, processor_id):
        # Initialise with common authentication keys
        api_key = self.api_key
        api_secret_key = self.api_secret_key
        access_token = self.access_token
        access_token_secret = self.access_token_secret

        # Extract the authentication keys from specified processor
        if (self.searching is not None):
            politicians = self.searching[constants.JSON_POLITICIANS_PROP]
            if (politicians is not None):
                processor = politicians["processor".format(processor_id)]
                if (processor is not None):
                    api_key = processor[constants.JSON_AUTHEN_PROP][constants.JSON_API_KEY_PROP]
                    api_secret_key = processor[constants.JSON_AUTHEN_PROP][constants.JSON_API_SECRET_KEY_PROP]
                    access_token = processor[constants.JSON_AUTHEN_PROP][constants.JSON_ACCESS_TOKEN_PROP]
                    access_token_secret = processor[constants.JSON_AUTHEN_PROP][constants.JSON_ACCESS_TOKEN_SECRET]

        return api_key, api_secret_key, access_token, access_token_secret
