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

def search_handles(stock, handle_list, start_date=None, end_date=None):
	# if end_date is None:
	# 	end_date = datetime.datetime.now().strftime('%Y-%m-%d')
	# 	print end_date

	for handle in handle_list:
		query = '%s+from=%s+since=%s+until=%s' % (stock, handle, start_date, end_date)
		search = api.GetSearch(term=query, lang='en')

		for t in search:
			print "\n\n"
			print t.user.screen_name + '(' + t.created_at + ')'
			print "\n", t.text
			print "\n", t.id
			print "\n"
			for url in t.urls:
				print url.expanded_url
				print url.url
			print "\n\n"
		print len(search)

	# add to database


