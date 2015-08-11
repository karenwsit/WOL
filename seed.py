"""Utility file to seed database from twitter api"""


from model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, TweetSentiment, connect_to_db, db
from server import app
from datetime import datetime
