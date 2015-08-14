import os
import datetime
import twitter
from model import TwitterHandle, Stock, connect_to_db, db
from server import app

#Twitter OAuth
#Pulling twitter_consumer_key from my environment. Environ is a dictionary. os.environ accesses specific environment 

api = twitter.Api(
	consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def search_todays_tweets():
	"""Given stock name, return queried tweets from a list of twitter handles for today & save to the database"""

	twitterhandle_tuplist = TwitterHandle.query.with_entities(TwitterHandle.twitterhandle_name).all() #returns list of twitterhandle tuples
	twitterhandle_list = [tup[0] for tup in twitterhandle_tuplist]

	stock_tuplist = Stock.query.with_entities(Stock.stock_name).all() #returns list of stock tuples
	stock_list = [tup[0] for tup in stock_tuplist]

	today_datetime = datetime.datetime.now()
	end_date = today_datetime.strftime('%Y-%m-%d')

	yesterday_datetime = datetime.datetime.now() - datetime.timedelta(hours=24)
	start_date = yesterday_datetime.strftime('%Y-%m-%d')

	#must have a more efficient way to call this function below:

	half_twitterhandle_list = twitterhandle_list[:2]
	print half_twitterhandle_list

	for stock in stock_list:   
		for handle in half_twitterhandle_list:
			query = '%s+from=%s+since=%s+until=%s' % (stock, handle, start_date, end_date)
			search = api.GetSearch(term=query, lang='en')
	print search

		# for t in search:	
		# 	tweet_created_at = t.created_at
		# 	tweet_txt = t.text
		# 	twitterhandle = TwitterHandle.query.filter_by(username=username).first()
		# 	if twitterhandle:
		# 		twitterhandle_id = twitterhandle.id
		# 	for url in t.urls:
		# 		tweet_url = url.url

	# 	#Adding tweets to my DB
	# 	new_tweet = Tweet(tweet_created_at=tweet_created_at, tweet_txt=tweet_txt,  tweet_url=tweet_url, twitterhandle_id=twitterhandle_id)
	# 	db.session.add(new_tweet)

	# db.session.commit()	


if __name__ == "__main__":
	connect_to_db(app)	



