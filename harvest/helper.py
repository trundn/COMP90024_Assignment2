# Provides various time-related functions
import time
# Implements classes to read and write tabular data in CSV format
import csv
# An easy-to-use Python library for accessing the Twitter API
import tweepy
# The harvest constant definitions
import constants

class Helper(object):
    def is_track_match(self, tweet_text, tracks):
        result = False

        if (tweet_text):
            if any(key_word in tweet_text for key_word in tracks):
                result = True

        return result

    def get_followers(self, tweepy_api, user_name, max_count):
        # Initialize a list to hold all followers
        followers = []

        for page in tweepy.Cursor(tweepy_api.followers,
                            screen_name = user_name,
                            wait_on_rate_limit = True,
                            count = constants.LIMIT_COUNT_PER_REQ).pages():
            
            try:
                # Put all new follower into final follower list
                followers.extend(page)

                # Check if total followers reached max count or not
                if ((max_count != -1) and (len(followers) >= max_count)):
                    break
            except tweepy.TweepError as ex:
                print("Going to sleep:", ex)
                # Sleep 60 seconds to avoid rate limit issue
                time.sleep(constants.ONE_MINUTE)

            # Sleep 60 seconds to avoid rate limit issue
            time.sleep(constants.ONE_MINUTE)

        return followers

    def get_all_tweets(self, tweepy_api, screen_name):
        # Initialize a list to hold all the tweepy Tweets
        alltweets = []

        try:
            # Make initial request for most recent tweets
            new_tweets = tweepy_api.user_timeline(screen_name = screen_name,
                count = constants.LIMIT_COUNT_PER_REQ)
            
            # Put all new tweets into final tweets list
            alltweets.extend(new_tweets)
            
            if (len(new_tweets) > 0):
                # Save the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1
                
                # Keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0:
                    time.sleep(constants.TWO_SECONDS)
                    
                    # All subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = tweepy_api.user_timeline(screen_name = screen_name,
                        count = constants.LIMIT_COUNT_PER_REQ, max_id = oldest)
                    
                    # Put all new tweets into final tweets list
                    alltweets.extend(new_tweets)
                    
                    # Update the id of the oldest tweet less one
                    oldest = alltweets[-1].id - 1
        except tweepy.TweepError as ex:
            print(ex)

        return alltweets