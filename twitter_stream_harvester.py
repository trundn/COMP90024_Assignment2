# %%

import tweepy
import sys
import couchdb
import json


# TODO: remove duplicate json

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)
        db.save(status._json)

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


# %%

# auth
consumer_key = 'Tlq2IBLkARdXDcSQNvIJY1SBZ'
consumer_secret = 'snhD9YyXP3VBGmxlfSnib3VQTxODoSs5LjP7jUpfz9n9nQPXHm'
access_token = '1251695031536152576-m1jDuNgpjUVDbfUL9j4uYS2Q38J3Ca'
access_token_secret = 'g6unv33TaFzoOdvikrfheHs1o69lry6yCMW8lZkvc0TFc'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# %%

# start db and creat document
try:
    couch = couchdb.Server('http://admin:admin@localhost:5984')
    db = couch['tweet']
except Exception:
    db = couch.create('tweet')

# %%

# standard: 400 keywords, 5,000 userids and 25 location boxes

locations = {"Australia": [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]}

# keywords
tags = ["covid", "COVID", "covid19", "COVID19", "covid-19", "COVID-19", "coronavirus", "CORONAVIRUS", "pandemic",
        "PANDEMIC", "epidemic", "EPIDEMIC"]
languages = ["en"]

# %%

# initialize stream
streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
stream.filter(track=tags, locations=locations["Australia"], languages=languages)
