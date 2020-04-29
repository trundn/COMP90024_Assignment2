# An easy-to-use Python library for accessing the Twitter API
import tweepy

class APIFactory(object):
    def __init__(self, config_loader):
        self.config_loader = config_loader

    def create_api(self):
        if not (self.config_loader.api_key and self.config_loader.api_secret_key and self.config_loader.access_token and self.config_loader.access_token_secret):
            raise RuntimeError("The authentication keys are missing.")

        # Creating the authentication object
        print("Creating OAuth user authentication.")
        auth = tweepy.OAuthHandler(self.config_loader.api_key, self.config_loader.api_secret_key)

        if (auth):
            # Setting your access token and secret
            auth.set_access_token(self.config_loader.access_token, self.config_loader.access_token_secret)
            
            # Creating the API object while passing in auth information
            print("Creating Tweepy API from OAuth user authentication.")
            api = tweepy.API(auth, wait_on_rate_limit = True)

            if (not api):
                raise RuntimeError("Cannot create Tweepy API.")
        else:
            raise RuntimeError("Cannot create OAuth user authentication.")

        return api