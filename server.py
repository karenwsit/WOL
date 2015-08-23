from flask import Flask, render_template
import datetime 
import urllib2, urllib, json

app = Flask(__name__)


@app.route("/")
def index():

	"""Loads main page"""

	return render_template("index.html")

@app.route("/stockprice")
def stockprice():

	today_datetime = datetime.datetime.now()
	end_date = today_datetime.strftime('%Y-%m-%d')

	yesterday_datetime = datetime.datetime.now() - datetime.timedelta(hours=24)
	start_date = yesterday_datetime.strftime('%Y-%m-%d')

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

	stocks.jsonify

	# for key in stocks:
	stock_ticker = 'FB'

	yql_url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%27"+stock_ticker+"%27%20and%20startDate%20%3D%20%27"+start_date+"%27%20and%20endDate%20%3D%20%27"+end_date+"%27&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="" """ 
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)

	# stock_dict = data['query']['results']

	# stock_date = stock_dict['quote']['Date']
	# stock_ticker = stock_dict['quote']['Symbol']
	# stock_close = stock_dict['quote']['Close']
	


if __name__ == "__main__":
	app.run(debug=True)
