import os
import datetime
import twitter

#Twitter OAuth
#Pulling twitter_consumer_key from my environment. Environ is a dictionary. os.environ accesses specific environment 

api = twitter.Api(
	consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])






