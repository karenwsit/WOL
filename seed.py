"""Utility file to seed database from twitter api"""


from model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, TweetSentiment, connect_to_db, db
from server import app
from datetime import datetime


stocks = {
	'GOOG' : 'Google',
	'TSLA' : 'Tesla',
	'CMG' : 'Chipotle',
	'DIS' : 'Disney',
	'AAPL' : 'Apple',
	'NKE' : 'Nike',
	'BABA' : 'Alibaba',
	'MSFT' : 'Microsoft',
	'TWTR' : 'Twitter',
}

def load_twitterhandles():
	"""Loads twitterhandles from twitterhandles.txt into database"""

	twitterhandle_file = open("twitterhandles.txt")
	twitterhandle_data = twitterhandle_file.read().split("\n")
	for line in twitterhandle_data:
		twitterhandle_list = line.split(",")
		twitterhandle_name = twitterhandle_list[0]
		twitterhandle_type = twitterhandle_list[1]
		
		new_twitterhandle = TwitterHandle(twitterhandle_name=twitterhandle_name, twitterhandle_type=twitterhandle_type)
		db.session.add(new_twitterhandle)

	db.session.commit()

def load_stocks():
	"""Loads stocks from stocks' dictionary into database"""

	for stockticker_id in stocks:
		stock_name = stocks[stockticker_id]
		
		new_stock = Stock(stockticker_id=stockticker_id, stock_name=stock_name)
		db.session.add(new_stock)

	db.session.commit()


def search_todays_tweets(stock=None, handle_list=None, start_date=None, end_date=None):
	"""Given stock name, return queried tweets from a list of twitter handles for today & save to the database"""

	handle_list = TwitterHandle.query.filter_by(username=username).all()
	print handle_list

	# for handle in handle_list:
	# 	query = '%s+from=%s+since=%s+until=%s' % (stock, handle, start_date, end_date)
	# 	search = api.GetSearch(term=query, lang='en')

	# 	for t in search:		
	# 		tweet_id = t.id
	# 		tweet_created_at = t.created_at
	# 		tweet_txt = t.text
	# 		twitterhandle = TwitterHandle.query.filter_by(username=username).first()
	# 		if twitterhandle:
	# 			twitterhandle_id = twitterhandle.id
	# 		for url in t.urls:
	# 			tweet_url = url.url

	# 	#Adding tweets to my DB
	# 	new_tweet = Tweet(tweet_id=tweet_id, tweet_created_at=tweet_created_at, tweet_txt=tweet_txt,  tweet_url=tweet_url, twitterhandle_id=twitterhandle_id)
	# 	db.session.add(new_tweet)

	# db.session.commit()		


# if __name__ == "__main__":
# 	connect_to_db(app)
# 	db.create_all()

# 	load_twitterhandles()
# 	load_stocks()
# 	search_todays_tweets("Google",["wsj"])








