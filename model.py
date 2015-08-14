"""Models and database functions for WOL project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#Model definitions 

class User(db.Model):
	"""User of WOL website."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key = True)

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<User user_id=%s>" % (self.user_id)

class Stock(db.Model):
	"""Stock on WOL website."""

	__tablename__ = "stocks"

	stockticker_id = db.Column(db.String(10), primary_key=True)
	stock_name = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<Stock stockticker_id=%s stock_name=%s>" % (self.stockticker_id, self.stock_name)

class UserStock(db.Model):
	"""Reference table for User and Stock"""

	__tablename__ = "userstocks"

	userstock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	stocticker_id = db.Column(db.String(10), db.ForeignKey('stocks.stockticker_id'))	

	#Define relationship to user
	user = db.relationship("User", backref=db.backref("userstocks", order_by=userstock_id))

	#Define relationship to stock
	stock = db.relationship("Stock", backref=db.backref("userstocks", order_by=userstock_id))

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<UserStock userstock_id=%s user_id=%s stockticker_id=%s>" % (self.userstock_id, self.user_id, self.stockticker_id)

class TwitterHandle(db.Model):
	"""TwitterHandle to query from"""

	__tablename__ = "twitterhandles"

	twitterhandle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	twitterhandle_name = db.Column(db.String(32), nullable=False)
	twitterhandle_type = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<TwitterHandle twitterhandle_id=%s twitterhandle_name=%s twitterhandle_type=%s>" % (self.twitterhandle_id, self.twitterhandle_name, self.twitterhandle_type)

class Tweet(db.Model):
	"""Queried tweets from twitterhandles"""

	__tablename__ = "tweets"

	tweet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	tweet_created_at = db.Column(db.String(32), nullable=False)
	tweet_txt = db.Column(db.String(150), nullable=False)
	tweet_url = db.Column(db.String(150))
	stockticker_id = db.Column(db.String(10), db.ForeignKey('stocks.stockticker_id'))
	twitterhandle_id = db.Column(db.Integer, db.ForeignKey('twitterhandles.twitterhandle_id'))

	#Define relationship to stock
	stock = db.relationship("Stock", backref=db.backref("tweets", order_by=tweet_id))

	#Define relaionship twitterhandle
	twitterhandle = db.relationship("TwitterHandle", backref=db.backref("tweets", order_by=tweet_id))

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<Tweet tweet_id=%s tweet_created_at=%s tweet_txt=%s tweet_url=%s stockticker_id=%s twitterhandle_id=%s>" % (self.tweet_id, self.tweet_created_at, self.tweet_txt, self.tweet_url, self.stockticker_id, self.twitterhandle_id)

class Sentiment(db.Model):
	"""Sentiment for each day"""

	__tablename__ = "sentiments"

	sentiment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	sentiment = db.Column(db.Boolean, nullable=False)
	likelihood_probability = db.Column(db.Float, nullable=False)

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<Sentiment sentiment_id=%s start_date=%s end_date=%s sentiment=%s likelihood_probability=%s>" % (self.sentiment_id, self.start_date, self.end_date, self.sentiment, self.likelihood_probability)

class TweetSentiment(db.Model):
	"""Reference table for Tweet and Sentiment"""

	__tablename__ = "tweetsentiments"

	tweetsentiment_id = db.Column(db.Integer, primary_key=True)
	tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.tweet_id'))
	sentiment_id = db.Column(db.Integer, db.ForeignKey('sentiments.sentiment_id'))

	#Define relaionship to tweet
	tweet = db.relationship("Tweet", backref=db.backref("tweetsentiments", order_by=tweetsentiment_id))

	#Define relaionship to sentiment
	sentiment = db.relationship("Sentiment", backref=db.backref("tweetsentiments", order_by=tweetsentiment_id))

	def __repr__(self):
		"""Provides helpful representation when printed"""
		return "<TweetSentiment tweetsentiment_id=%s tweet_id=%s sentiment_id=%s>" % (self.tweetsentiment_id, self.tweet_id, self.sentiment_id)

##########################################################################

def connect_to_db(app):
	"""Connect database to Flask app."""

	#Configure to use SQLite database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wol.db'
	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print "Connected to DB."

















