from flask import Flask, render_template, jsonify, send_from_directory, request
from models.model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, connect_to_db, db, StockPrice
import datetime, time
import requests
from sqlalchemy.sql import func
import numpy
from util.jsonbuilder import JsonBuilder

app = Flask(__name__, static_url_path='')

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
DATE_FORMAT = '%Y-%m-%d'
POSITIVE = 'POSITIVE'
NEGATIVE = 'NEGATIVE'


@app.route("/")
def index():

    return render_template('index.html')


@app.route("/json")
def make_json_object():

    json_instance = JsonBuilder()
    json_object = jsonify(json_instance.get_json())
    return json_object


def get_stockprice(stock_ticker=None):

    stockprice_url_template = 'http://finance.yahoo.com/webservice/v1/symbols/{0}/quote?format=json'
    stockprice_url = stockprice_url_template.format(stock_ticker)
    req = requests.get(stockprice_url)
    data = req.json()
    return data['list']['resources'][0]['resource']['fields']['price']


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
