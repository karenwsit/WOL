import os
import datetime
import twitter


api = twitter.Api(
	consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

#pulling from my environment the twitter_consumer_key. Environ is a dictionary! os.environ accessing specific environment
#print os.environ

def search_handles(stock='Google', handle_list=['wsj'], start_date=None, end_date=None):
	# if end_date is None:
	# 	end_date = datetime.datetime.now().strftime('%Y-%m-%d')
	# 	print end_date

	for handle in handle_list:
		query = '%s+from:%s since:2015-07-01' % (stock, handle)
		search = api.GetSearch(term=query, lang='en', until=end_date) 
		# add to database
		for t in search:
			print "\n\n"
			print t.user.screen_name + '(' + t.created_at + ')'
			print "\n", t
			print "\n\n"
		print len(search)



# search_handles("Yahoo",["wsj"])