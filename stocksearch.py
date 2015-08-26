import urllib2, urllib, json
import datetime
import pprint

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

#looping through stocks list & calling the Yahoo Finance API 

def get_todays_stockprice():

	# today_datetime = datetime.datetime.now()
	# end_date = today_datetime.strftime('%Y-%m-%d')

	# yesterday_datetime = datetime.datetime.now() - datetime.timedelta(hours=24)
	# start_date = yesterday_datetime.strftime('%Y-%m-%d')

	for key in stocks:
		stock_ticker = key

		# yql_url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%27"+stock_ticker+"%27%20and%20startDate%20%3D%20%27"+start_date+"%27%20and%20endDate%20%3D%20%27"+end_date+"%27&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=" 
		yql_url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22"+stock_ticker+"%22%20and%20startDate%20%3D%20%222015-07-17%22%20and%20endDate%20%3D%20%222015-08-17%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

		result = urllib2.urlopen(yql_url).read()
		data = json.loads(result)

		stock_dict = data['query']['results']
		stock_dict_value = stock_dict['quote']

		for i in range(len(stock_dict_value)):
			stock_date = stock_dict_value[i]['Date']
			stock_ticker = stock_dict_value[i]['Symbol']
			stock_close = stock_dict_value[i]['Close']

			print stock_date
			print stock_ticker
			print stock_close

get_todays_stockprice()

