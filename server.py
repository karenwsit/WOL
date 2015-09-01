from flask import Flask, render_template, jsonify, send_from_directory, request
from model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, connect_to_db, db, StockPrice
import datetime, time
import urllib2, urllib, json
from urllib2 import Request, urlopen 
from sqlalchemy.sql import func
import numpy

app = Flask(__name__, static_url_path='')

stocks = {
	'GOOG' : 'Google',
	'TSLA' : 'Tesla',
	'CMG' : 'Chipotle',
	'DIS' : 'Disney',
	'AAPL' : 'Apple',
	'NKE' : 'Nike',
	'BABA' : 'Alibaba', 
	'MSFT' : 'Microsoft',
	'TWTR' : 'Twitter',
	'FB' : 'Facebook'
	}
DATE_FORMAT = '%Y-%m-%d'
POSITIVE = 'POSITIVE'
NEGATIVE = 'NEGATIVE'

@app.route("/")
def index():

	"""Loads main page"""

	return render_template('index.html')


@app.route("/static/<path:file_name>")
def static_files(file_name):

	return send_from_directory('static', file_name)


@app.route("/json")
def make_json_object():
	main_list = []
	# start = request.args.get("startDate")
	start = '2015-07-20'
	end = request.args.get("endDate")

	start_date = datetime.datetime.strptime(start,(DATE_FORMAT))

	end_date = datetime.datetime.strptime(end,(DATE_FORMAT))
	day_count = (end_date - start_date).days + 1

	for ticker, name in stocks.iteritems():
		ticker_dict = {
			'name': name,
			'dates': {},
			'current_stock_price': 0
			#'current_stock_price' : get_stockprice(ticker)
		} 

		date_dict = ticker_dict['dates']
		# import pprint; pprint.pprint(ticker_dict)


		probability_list = []


		for single_date in (start_date + datetime.timedelta(n) for n in range(day_count)):

			unix_date = time.mktime(single_date.timetuple())
			first_date = single_date.strftime(DATE_FORMAT)
			second_date = (single_date + datetime.timedelta(1)).strftime(DATE_FORMAT)
			tweets = db.session.query(Tweet).filter(Tweet.tweet_created_at.between(first_date, second_date)).filter_by(stockticker_id=name).all()
			historical_stock_price_obj = db.session.query(StockPrice).filter(StockPrice.date.between(first_date,second_date)).filter_by(stockticker_id=ticker).all()  # is a list, but asking for only 1 date

			if len(historical_stock_price_obj) > 0:
				historical_stock_price = historical_stock_price_obj[0].stock_price 
			
			if len(tweets) != 0:
				date_dict[first_date] = {
					'unix_time' : unix_date,
					'historical_stock_price': historical_stock_price,
					'probability_avg' : numpy.mean([tweet.likelihood_probability for tweet in tweets]),
					'probability_median' : numpy.median([tweet.likelihood_probability for tweet in tweets]),
					'standard_dev' : numpy.std([tweet.likelihood_probability for tweet in tweets]),
					'tweets': [{'text': tweet.raw_tweet_text,'url' : tweet.tweet_url} for tweet in tweets]
				}
				probability_list.append(date_dict[first_date]['probability_avg'])

		ticker_dict['overall_prob'] = numpy.mean(probability_list)
		ticker_dict['overall_sentiment'] = POSITIVE if ticker_dict['overall_prob'] >= .5 else NEGATIVE

		main_list.append(ticker_dict)

	# import pprint; pprint.pprint({'data': main_list})

	json_object = jsonify({'data': main_list})

	return json_object

def get_stockprice(stock_ticker=None):

	stockprice_url_template = 'http://finance.yahoo.com/webservice/v1/symbols/{0}/quote?format=json'
	stockprice_url = stockprice_url_template.format(stock_ticker)

	req = Request(stockprice_url)
	result_str = urlopen(req)
	data = json.loads(result_str.read())

	return data['list']['resources'][0]['resource']['fields']['price']


if __name__ == "__main__":
	connect_to_db(app)
	app.run(debug=True)

