import json
import urllib
import pprint

consumer_key=os.environ.get('KIMONO_CONSUMER_KEY')

my_results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/2lgdxjpq?apikey=%s"% consumer_key)) 

stock = my_results['name']
time_ago = my_results['results']['collection1'][0]['timeago']
tweet = my_results ['results']
print time_ago


pprint.pprint(results)
# for tweet in results:
# 	pprint.pprint(tweet)
# 	break


# new_tweet = Tweet(tweet_created_at=tweet_created_at, tweet_txt=tweet_txt,  tweet_url=tweet_url, twitterhandle_id=twitterhandle_id)