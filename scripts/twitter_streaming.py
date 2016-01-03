from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# twitter OAuth process
auth = OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))