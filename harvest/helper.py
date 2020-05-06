# Provides various time-related functions
import time
# Implements classes to read and write tabular data in CSV format
import csv
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions

# Sentimental anaylsis for extracting positve, negative, neutral, compound emotion
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

class Helper(object):
    def is_track_match(self, tweet_text, tracks):
        result = False

        if (tweet_text):
            if any(key_word in tweet_text for key_word in tracks):
                result = True

        return result

    def extract_coordinates(self, tweet):
        source = ""
        coordinates = []

        if (tweet is not None):
            if ((tweet.geo is not None) and (tweet.geo.coordinates is not None)):
                source = harvest.constants.GEO
                coordinates = tweet.geo.coordinates
            elif ((tweet.coordinates is not None) and (tweet.coordinates.coordinates is not None)):
                source = harvest.constants.COORDINATES
                coordinates = [tweet.coordinates.coordinates[1], tweet.coordinates.coordinates[0]]
            elif ((tweet.place is not None) and (tweet.place.bounding_box is not None) and (tweet.place.bounding_box.coordinates is not None)):
                source = harvest.constants.PLACE
                tmp_coordinates = tweet.place.bounding_box.coordinates[0]
                latitude = (tmp_coordinates[0][1] + tmp_coordinates[1][1]) / 2
                longitude =(tmp_coordinates[0][0] + tmp_coordinates[2][0]) / 2
                coordinates = [latitude, longitude]

        return source, coordinates


    def get_followers(self, tweepy_api, user_name, max_count):
        # Initialize a list to hold all followers
        followers = []

        for page in tweepy.Cursor(tweepy_api.followers,
                            screen_name = user_name,
                            wait_on_rate_limit = True,
                            count = harvest.constants.LIMIT_COUNT_PER_REQ).pages():
            
            try:
                # Put all new follower into final follower list
                followers.extend(page)

                # Check if total followers reached max count or not
                if ((max_count != -1) and (len(followers) >= max_count)):
                    break
            except tweepy.TweepError as ex:
                print("Going to sleep:", ex)
                # Sleep 60 seconds to avoid rate limit issue
                time.sleep(harvest.constants.ONE_MINUTE)

            # Sleep 60 seconds to avoid rate limit issue
            time.sleep(harvest.constants.ONE_MINUTE)

        return followers

    def get_all_tweets(self, tweepy_api, screen_name):
        # Initialize a list to hold all the tweepy Tweets
        alltweets = []

        try:
            # Make initial request for most recent tweets
            new_tweets = tweepy_api.user_timeline(screen_name = screen_name,
                count = harvest.constants.LIMIT_COUNT_PER_REQ)
            
            # Put all new tweets into final tweets list
            alltweets.extend(new_tweets)
            
            if (len(new_tweets) > 0):
                # Save the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1
                
                # Keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0:
                    time.sleep(harvest.constants.TWO_SECONDS)
                    
                    # All subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = tweepy_api.user_timeline(screen_name = screen_name,
                        count = harvest.constants.LIMIT_COUNT_PER_REQ, max_id = oldest)
                    
                    # Put all new tweets into final tweets list
                    alltweets.extend(new_tweets)
                    
                    # Update the id of the oldest tweet less one
                    oldest = alltweets[-1].id - 1
        except tweepy.TweepError as ex:
            print(ex)

        return alltweets

    def extract_emotions(self, tweet_text):
        # A SentimentIntensityAnalyzer
        sia = SIA()
        # Get emotion scores e.g.: {'neg': 0.047, 'neu': 0.849, 'pos': 0.104, 'compound': 0.3565}
        emotions = sia.polarity_scores(tweet_text)
        return emotions
