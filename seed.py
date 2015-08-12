"""Utility file to seed database from twitter api"""


from model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, TweetSentiment, connect_to_db, db
from server import app
from datetime import datetime

def load_twitterhandles():
	"""Loads twitterhandles from twitterhandles.txt into database"""

	twitterhandle_file = open("twitterhandles.txt")
	twitterhandle_data = twitterhandle_file.read().split("\n")