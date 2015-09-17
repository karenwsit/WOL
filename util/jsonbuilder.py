#PUT THE JSON BUILDER CLASS IN HERE

class JsonBuilder(object):


	start = '2015-07-20'
	end = request.args.get("endDate")
	start_date = datetime.datetime.strptime(start,(DATE_FORMAT))
	end_date = datetime.datetime.strptime(end,(DATE_FORMAT))
	day_count = (end_date - start_date).days + 1

	
	def __init__(self):
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
		pass 
	# where are stocks coming from
	for ticker, name in stocks.iteritems():
        ticker_dict = {
            'name': name,
            'dates': {},
            'current_stock_price' : get_stockprice(ticker)
        } 
        date_dict = ticker_dict['dates']

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
