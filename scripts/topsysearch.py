import json
import urllib
import os
import pprint

consumer_key=os.environ.get('KIMONO_CONSUMER_KEY')
api_ids = ['2lgdxjpq','awexe96c','9a7rbjs4','9r4xnuiq']

for api_id in api_ids:
	my_results = json.load(urllib.urlopen(
		"https://www.kimonolabs.com/api/%s?apikey=%s" % (api_id, consumer_key))
	)

	def load_tweets():
		collection1_list = my_results['results']['collection1']
		stock_ticker = Stock.query.filter_by(name=my_results['name']).first()
		if stock_ticker:
			stock_ticker_id = stock_ticker.name

		for i in collection1_list:
			tweet_created_at = i['timeago']['text']
			tweet_txt = i['tweet']['text']
			tweet_url = i['timeago']['href']
			twitter_handle = TwitterHandle.query.filter_by(username=i['twitterhandle']['text']).first()
			if twitter_handle:
				twitterhandle_id = twitter_handle.id 
		
			new_tweet = Tweet(
				tweet_created_at=tweet_created_at,
				tweet_txt=tweet_txt,
				tweet_url=tweet_url,
				twitterhandle_id=twitterhandle_id,
				stock_ticker_id=stock_ticker_id)

load_tweets()