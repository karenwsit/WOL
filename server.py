from flask import Flask, render_template, jsonify, send_from_directory
from model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, connect_to_db, db, StockPrice
import datetime
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
	start_date = datetime.datetime.strptime('2015-07-19',(DATE_FORMAT))
	end_date = datetime.datetime.strptime('2015-08-21',(DATE_FORMAT))
	day_count = (end_date - start_date).days + 1

	for ticker, name in stocks.iteritems():
		ticker_dict = {
			'name': name,
			'dates': {}
		} 

		date_dict = ticker_dict['dates']
		#import pprint; pprint.pprint(ticker_dict)
		for single_date in (start_date + datetime.timedelta(n) for n in range(day_count)): 
			first_date = single_date.strftime(DATE_FORMAT)
			second_date = (single_date + datetime.timedelta(1)).strftime(DATE_FORMAT)
			tweets = db.session.query(Tweet).filter(Tweet.tweet_created_at.between(first_date, second_date)).filter_by(stockticker_id=name).all()
			if len(tweets) != 0:
				date_dict[first_date] = {
					'probability_avg': numpy.mean([tweet.likelihood_probability for tweet in tweets]),
					'probability_median' : numpy.median([tweet.likelihood_probability for tweet in tweets]),
					'standard_dev' : numpy.std([tweet.likelihood_probability for tweet in tweets]),
					'tweets': [{'text': tweet.raw_tweet_text,'url' : tweet.tweet_url} for tweet in tweets]
				}

		main_list.append(ticker_dict)

	json_object = jsonify({'data': main_list})	
	return json_object

@app.route("/stockprice")
@app.route("/stockprice/<stock_ticker>")
def stockprice(stock_ticker=None):

	current_price_dict = {}
	stockprice_url_template = 'http://finance.yahoo.com/webservice/v1/symbols/{0}/quote?format=json'

	def get_stockdata(stock):
		stockprice_url = stockprice_url_template.format(stock)

		req = Request(stockprice_url)
		result_str = urlopen(req)
		data = json.loads(result_str.read())
		print data
		all_current_prices = current_price_dict[stock] = data['list']['resources'][0]['resource']['fields']['price']
		print all_current_prices

	if stock_ticker is None:
		for key in stocks:
			get_stockdata(key)			
	else: 
		get_stockdata(stock_ticker)

	json_object = jsonify(current_price_dict)
	return json_object


if __name__ == "__main__":
	connect_to_db(app)
	app.run(debug=True)

