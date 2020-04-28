# %%

import tweepy
import sys
import couchdb
import json

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
couch = couchdb.Server('http://admin:admin@localhost:5984')
try:
    db = couch['scottmorrison']
except Exception:
    db = couch.create('scottmorrison')

# count max = 200
# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
t_ScottMorrisonMP = api.user_timeline('ScottMorrisonMP', count=200)
for tweet in t_ScottMorrisonMP:
    db.save(tweet._json)

# %%

### Victoria
# start db and creat document
try:
    couch = couchdb.Server('http://admin:admin@localhost:5984')
    db = couch['danielandrews']
except:
    db = couch.create('danielandrews')

# count max = 200
# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
t_DanielAndrewsMP = api.user_timeline('DanielAndrewsMP', count=200)
for tweet in t_DanielAndrewsMP:
    db.save(tweet._json)

# %%

### NSW
# start db and creat document
try:
    couch = couchdb.Server('http://admin:admin@localhost:5984')
    db = couch['gladysberejiklian']
except:
    db = couch.create('gladysberejiklian')

# count max = 200
# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
t_GladysB = api.user_timeline('GladysB', count=200)
for tweet in t_GladysB:
    db.save(tweet._json)

# %%

### Queensland
# start db and creat document
try:
    couch = couchdb.Server('http://admin:admin@localhost:5984')
    db = couch['annastaciapalaszczuk']
except:
    db = couch.create('annastaciapalaszczuk')

# count max = 200
# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
t_AnnastaciaMP = api.user_timeline('AnnastaciaMP', count=200)
for tweet in t_AnnastaciaMP:
    db.save(tweet._json)

# %%

# @MarkMcGowanMP
### WA
# start db and creat document
try:
    couch = couchdb.Server('http://admin:admin@localhost:5984')
    db = couch['markmcgowan']
except:
    db = couch.create('markmcgowan')

# count max = 200
# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
t_MarkMcGowanMP = api.user_timeline('MarkMcGowanMP', count=200)
for tweet in t_MarkMcGowanMP:
    db.save(tweet._json)
