import os
import twitter


api = twitter.Api(
	consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

#pulling from my environment the twitter_consumer_key. Environ is a dictionary! os.environ accessing specific environment
#print os.environ

def search_handles(stock, handle_list):
	for handle in handle_list:
		query = '%s+from:%s' % (stock, handle)
		search = api.GetSearch(term=query, lang='en') 
		# add to database
		for t in search:
			print "\n\n"
			print t.user.screen_name + '(' + t.created_at + ')'
			print "\n", t
			print "\n\n"
		print len(search)

# +since:2015-08-03+until:2015-08-04
