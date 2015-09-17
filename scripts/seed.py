"""Utility file to seed database from twitter api"""

from model import Stock, TwitterHandle, Tweet, Sentiment, connect_to_db, db, StockPrice
from server import app
from datetime import datetime
import classifer
import os
import re
import decimal
from urllib2 import Request, urlopen
import urllib
import json


def load_twitterhandles():
    """Loads twitterhandles from twitterhandles.txt into database"""

    twitterhandle_file = open("twitterhandles.txt")
    twitterhandle_data = twitterhandle_file.read().split("\n")
    for line in twitterhandle_data:
        twitterhandle_list = line.split(", ")
        twitterhandle_name = twitterhandle_list[0]
        twitterhandle_type = twitterhandle_list[1]
        new_twitterhandle = TwitterHandle(twitterhandle_name=twitterhandle_name, twitterhandle_type=twitterhandle_type)
        db.session.add(new_twitterhandle)

    db.session.commit()

STOCKS = {
    'GOOG': 'Google',
    'TSLA': 'Tesla',
    'CMG': 'Chipotle',
    'DIS': 'Disney',
    'AAPL': 'Apple',
    'NKE': 'Nike',
    'BABA': 'Alibaba',
    'MSFT': 'Microsoft',
    'TWTR': 'Twitter',
    'FB': 'Facebook',
}


def load_stocks():
    """Loads stocks from stocks' dictionary into database"""

    for stockticker_id in STOCKS:
        stock_name = STOCKS[stockticker_id]
        new_stock = Stock(stockticker_id=stockticker_id, stock_name=stock_name)
        db.session.merge(new_stock)

    db.session.commit()


KIMONO_API_IDS = {
    'Google': ['2lgdxjpq', 'awexe96c', '9a7rbjs4', '9r4xnuiq'],
    'Tesla': ['3n9ge4xs'],
    'Chipotle': ['6w1fc7gq'],
    'Disney': ['awkdxbz6'],
    'Apple': ['3b2h1ezc', 'd61do17k', 'bglx9jqk', '6fmv92pk'],
    'Nike': ['5ejpmmty'],
    'Alibaba': ['clsw9yzo'],
    'Microsoft': ['cdtuqhxu', 'eacxst54'],
    'Twitter': ['bgodnive', '8hbdw9vo', '1xccxxk6'],
    'Facebook': ['8mhmw11c', '2bmg3uii', '66jhvw3g']
}


def load_tweets(api_ids=None):
    consumer_key = os.environ.get('KIMONO_CONSUMER_KEY')
    tweet_list = []

    for company_name, api_id_list in KIMONO_API_IDS.iteritems():
        for api_id in api_id_list:

            my_results = json.load(urllib.urlopen(
                "https://www.kimonolabs.com/api/%s?apikey=%s" % (api_id, consumer_key))
            )

            collection1_list = my_results['results']['collection1']
            stock_ticker = Stock.query.filter_by(stock_name=my_results['name']).first()
            if stock_ticker:
                stock_ticker_id = stock_ticker.stock_name

            for i in collection1_list:
                timestamp = i['timeago']['data-timestamp']
                tweet_created_at = datetime.fromtimestamp(int(timestamp))
                raw_tweet_text = i['tweet']['text']
                clean_tweet_text1 = re.sub(r"http\S+", "", raw_tweet_text)
                clean_tweet_text = re.sub(r"@\S+", "", clean_tweet_text1).replace('"','').replace(',','').replace('.','').strip()
                tweet_url = i['timeago']['href']
                twitter_handle_dirty = i['twitterhandle']['text']
                twitter_handle_clean = twitter_handle_dirty[twitter_handle_dirty.find('@')+1:]
                stock = Stock.query.filter_by(stock_name=company_name).first()
                if stock:
                    stockticker_id = stock.stockticker_id
                twitter_handle = TwitterHandle.query.filter_by(twitterhandle_name=twitter_handle_clean).first()
                if twitter_handle:
                    twitterhandle_id = twitter_handle.twitterhandle_id
                new_tweet = dict(
                    tweet_created_at=tweet_created_at,
                    raw_tweet_text=raw_tweet_text,
                    clean_tweet_text=clean_tweet_text,
                    tweet_url=tweet_url,
                    twitterhandle_id=twitterhandle_id,
                    stockticker_id=stock_ticker_id)
                tweet_list.append(new_tweet)

    db.engine.execute(Tweet.__table__.insert(), tweet_list)
    db.session.commit()


def load_sentiments_into_tweettable():
    tweet_classifier = classifer.get_trained_classifier()
    tweets = Tweet.query.all()

    for tweet in tweets:
        sentiment = tweet_classifier.classify(classifer.extract_features(tweet.clean_tweet_text.split()))
        classifier_object = tweet_classifier.prob_classify(classifer.extract_features(tweet.clean_tweet_text.split()))
        log_prob = classifier_object.logprob('positive')
        likelihood_probability = decimal.Decimal(pow(2, log_prob))
        tweet.sentiment = sentiment
        tweet.likelihood_probability = likelihood_probability

    db.session.commit()


def load_sentiments():
    new_sentiment1 = Sentiment(sentiment='positive')
    new_sentiment2 = Sentiment(sentiment='negative')

    db.session.add(new_sentiment1)
    db.session.add(new_sentiment2)
    db.session.commit()


def load_stockprices():

    for key in STOCKS:
        stock_ticker = key
        yql_url = """https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22"""+stock_ticker+"""%22%20and%20startDate%20%3D%20%222015-07-17%22%20and%20endDate%20%3D%20%222015-08-17%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="""
        req = Request(yql_url)
        result_str = urlopen(req)
        data = json.loads(result_str.read())

        stock_dict = data['query']['results']
        stock_dict_value = stock_dict['quote']

        for i in range(len(stock_dict_value)):
            stock_date_string = stock_dict_value[i]['Date']
            stock_date = datetime.strptime(stock_date_string, "%Y-%m-%d")
            stock_ticker = stock_dict_value[i]['Symbol']
            stock_close = stock_dict_value[i]['Close']

            new_stockprice = StockPrice(
                stockticker_id=stock_ticker,
                date=stock_date,
                stock_price=stock_close)

            db.session.add(new_stockprice)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_sentiments_into_tweettable()
