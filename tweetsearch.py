import os
import datetime
# import twitter
import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from model import TwitterHandle, Stock, connect_to_db, db
from server import app

#Twitter OAuth
#Pulling twitter_consumer_key from my environment. Environ is a dictionary. os.environ accesses specific environment 

# ck = os.environ.get('TWITTER_CONSUMER_KEY')
# cs = os.environ.get('TWITTER_CONSUMER_SECRET')
# print ck, "*************************************"
# print cs

# auth = OAuthHandler(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'), consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'))
# auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))



def date_range(start,end):
   current = start
   while (end - current).days >= 0:
      yield current
      current = current + datetime.timedelta(seconds=1)  

class TweetListener(StreamListener):
    def on_data(self, status):
        #api = tweepy.API(auth_handler=auth)
        #status.created_at += timedelta(hours=900)

        startDate = datetime.datetime(2015, 8, 10)
        stopDate = datetime.datetime(2015, 8, 11)
        for date in date_range(startDate,stopDate):
            status.created_at = date
            print "tweet " + str(status.created_at) 
            print status.text + "\n"  
            # You can dump your tweets into Json File, or load it to your database

stream = Stream(auth, TweetListener())
list_users = ['1754641']#Some ids
list_terms = ['Google']#Some terms
stream.filter(follow=list_users)
stream.filter(track=list_terms)

# class StdOutListener(StreamListener):

#     def on_data(self, data):
#         # process stream data here
#         print(data)

#     def on_error(self, status):
#         print(status)

# if __name__ == '__main__':
#     listener = StdOutListener()
#     twitterStream = Stream(auth, listener)
#     twitterStream.filter(follow=['575930104'])




# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

# api.search(q='test',since='2014-07-01',until='2014-07-31'):

def search_todays_tweets(stock='Google', handle='nytimesbusiness', end_date='2015-08-11', start_date='2015-08-10'):
	"""Given stock name, return queried tweets from a list of twitter handles for today & save to the database"""

	#returns list of twitterhandle tuples

	twitterhandle_tuplist = TwitterHandle.query.with_entities(TwitterHandle.twitterhandle_name).all() 
	twitterhandle_list = [tup[0] for tup in twitterhandle_tuplist]

	stock_tuplist = Stock.query.with_entities(Stock.stock_name).all() #returns list of stock tuples
	stock_list = [tup[0] for tup in stock_tuplist]

	# today_datetime = datetime.datetime.now()
	# end_date = today_datetime.strftime('%Y-%m-%d')

	# yesterday_datetime = datetime.datetime.now() - datetime.timedelta(hours=24)
	# start_date = yesterday_datetime.strftime('%Y-%m-%d')

	# stock = stock_list[0] 
	# half_twitterhandle_list = twitterhandle_list[:48]

	# for handle in half_twitterhandle_list:
	query = '%s+from=%s+since=%s+until=%s' % (stock, handle, start_date, end_date)
	# query = stock + "%20from%3A" + handle + "%20since%3A" + start_date + "%20until%3A" + end_date
	print query
	# 	q=Google%20from%3Anytimesbusiness%20since%3A2015-08-10%20until%3A2015-08-11&src=typd
	search = api.GetSearch(term=query, lang='en')
	print "SEARCH", search
	# 	for t in search:	
	# 		tweet_created_at = t.created_at
	# 		tweet_txt = t.text
	# 		twitterhandle = TwitterHandle.query.filter_by(username=username).first()
	# 		if twitterhandle:
	# 			twitterhandle_id = twitterhandle.id
	# 		for url in t.urls:
	# 			tweet_url = url.url

	# #Adding tweets to my DB
	# 	new_tweet = Tweet(tweet_created_at=tweet_created_at, tweet_txt=tweet_txt,  tweet_url=tweet_url, twitterhandle_id=twitterhandle_id)
	# 	db.session.add(new_tweet)

	# db.session.commit()	

	#must have a more efficient way to call this function below:



	# twitter_cons_keys_list = os.environ['TWITTER_CONSUMER_KEY'].split(",")
	# twitter_cons_secrets_list = os.environ['TWITTER_CONSUMER_SECRET'].split(",")
	# twitter_token_keys_list = os.environ['TWITTER_ACCESS_TOKEN_KEY'].split(",")
	# twitter_token_secrets_list = os.environ['TWITTER_ACCESS_TOKEN_SECRET'].split(",")

	# print twitter_cons_keys_list
	# print twitter_cons_secrets_list
	# print twitter_token_keys_list
	# print twitter_token_secrets_list

	# print "cons_key", twitter_cons_keys_list[0]
	# print "secret key", twitter_cons_secrets_list[0]
	# print "token", twitter_token_keys_list[0]
	# print "token secret", twitter_token_secrets_list[0]

	# for i in range(len(stock_list)): 

	# api = twitter.Api(
	# 	consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
	#     consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
	#     access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
	#     access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
 
	# for handle in twitterhandle_list:
	# 	query = '%s+from=%s+since=%s+until=%s' % (stock, handle, start_date, end_date)
	# 	search = api.GetSearch(term=query, lang='en')
	# print "SEARCH", search

		



if __name__ == "__main__":
	connect_to_db(app)
	# search_todays_tweets()



