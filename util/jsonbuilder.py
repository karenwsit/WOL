from flask import jsonify
from models.model import Tweet, db, StockPrice
import datetime
import time
import requests
import numpy


class JsonBuilder(object):

    DATE_FORMAT = '%Y-%m-%d'
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
        'FB': 'Facebook'
    }
    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'

    def __init__(self, start='2015-07-20', end='2015-08-17'):
        self.start_date = datetime.datetime.strptime(start, (JsonBuilder.DATE_FORMAT))
        self.end_date = datetime.datetime.strptime(end, (JsonBuilder.DATE_FORMAT))
        self.day_count = (self.end_date - self.start_date).days + 1

        self.json_object = self._create_json_object()

    def get_json(self):
        return self.json_object

    def _create_json_object(self):
        main_list = []
        for ticker, name in JsonBuilder.STOCKS.iteritems():
            ticker_dict = {
                'name': name,
                'dates': {},
                'current_stock_price': self._get_stockprice(ticker)
            }
            #a double assignment from the output of _create_data_dict_for_each_date function. ticker_dict['dates'] = date_dict & ticker_dict['overall_prob'] = sentiment_prob
            ticker_dict['dates'], ticker_dict['overall_prob'] = self._create_data_dict_for_each_date(ticker, name)
            ticker_dict['overall_sentiment'] = JsonBuilder.POSITIVE if ticker_dict['overall_prob'] >= .5 else JsonBuilder.NEGATIVE
            main_list.append(ticker_dict)

        json_object = {'data': main_list}

        return json_object

    def _create_data_dict_for_each_date(self, ticker, stock_name):
        probability_list = []
        date_dict = {}

        for single_date in (self.start_date + datetime.timedelta(n) for n in range(self.day_count)):

            unix_date = time.mktime(single_date.timetuple())
            first_date = single_date.strftime(JsonBuilder.DATE_FORMAT)
            second_date = (single_date + datetime.timedelta(1)).strftime(JsonBuilder.DATE_FORMAT)

            tweets = db.session.query(Tweet).filter(
                    Tweet.tweet_created_at.between(first_date, second_date)
                ).filter_by(
                    stockticker_id=stock_name
                ).all()

            historical_stock_price_obj = db.session.query(StockPrice).filter(
                    StockPrice.date.between(first_date, second_date)
                ).filter_by(
                    stockticker_id=ticker
                ).all()  # is a list, but asking for only 1 date

            if len(historical_stock_price_obj) > 0:
                historical_stock_price = historical_stock_price_obj[0].stock_price
            if len(tweets) != 0:
                date_dict[first_date] = {
                    'unix_time': unix_date,
                    'historical_stock_price': historical_stock_price,
                    'probability_avg': numpy.mean([tweet.likelihood_probability for tweet in tweets]),
                    'probability_median': numpy.median([tweet.likelihood_probability for tweet in tweets]),
                    'standard_dev': numpy.std([tweet.likelihood_probability for tweet in tweets]),
                    'tweets': [{'text': tweet.raw_tweet_text, 'url': tweet.tweet_url} for tweet in tweets]
                }
                probability_list.append(date_dict[first_date]['probability_avg'])
                sentiment_probability = numpy.mean(probability_list)

        return date_dict, sentiment_probability

    def _get_stockprice(self, stock_ticker=None):

        stockprice_url_template = 'http://finance.yahoo.com/webservice/v1/symbols/{0}/quote?format=json'
        stockprice_url = stockprice_url_template.format(stock_ticker)
        req = requests.get(stockprice_url)
        data = req.json()
        return data['list']['resources'][0]['resource']['fields']['price']
