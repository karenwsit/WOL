# WOL - the owl of wol street

![Logo](/static/img/WOLReadMeLogo.png)

### Overview
WOL is a fullstack web application that creates data visualizations of tweet sentiments of particular companies in a user's financial portfolio. Tweets are normalized, tokenized, and analyzed using natural language processing. Users are able to conduct exploratory visual analysis and view sentiment patterns/trends to ultimately help users decide when to buy or sell stocks.

![Overview](/static/img/WOLReadMeOverview.png)
 
### Technology Stack
Python, Sqlite3, SQLAlchemy, Flask, Natural Language Toolkit, Regex, Javascript, JQuery, DataTables plug-in for jQuery, Charts.JS, Bootstrap, HTML, CSS, Yahoo Finance API, Kimono Labs APIs: Topsy

### Twitter Data From Topsy
Historic tweets containing companies' names are searched and filtered from carefully curated list of 96 Twitter handles (news sources, market influencers, research)  from a social media aggregator site, Topsy.com. APIs to Topsy were created via Kimono Labs, an automated data extraction tool, and the tweets were then stored in SQLite. I chose Topsy instead of the Twitter API, because Twitter has a strict limit on API calls and can only retrieve tweets not older seven days.

### WOL's Sentiment Analysis Algorithm
WOL's sentiment analysis algorithm is calculated using Python's Natural Language Processing Toolkit library, which is: 

>A corpus data of 1.6 million preclassified positive & negative tweets from [Sentiment140](http://help.sentiment140.com/for-students) was used to train a Naives Bayes classifier. After the classifier is trained, a feature extractor dictionary was created, and the most relevant features were applied to the classifier. 

Each tweet is normalized using regular expressions to remove usernames and links. The tweet is then tokenized. Given the tweets features, a log probability is calculated for each possible label (positive or negative). The label with the highest probability determines whether or not a tweet is classified 'positive' or 'negative' through the Naives Bayes classifier. 

### Data Visualization with chart.Js & DataTables 
The log probability of the 'positive' label is plotted and graphed with Chart.js' scatter plot. Chart.js is an animated, interactive and HTML5 based JavaScript chart. The sentiment, sentiment probability, and current stock price of each company is displayed in DataTables, which is a table plug-in for jQuery. DataTables provides searching, sorting and pagination without any configuration.

![One Stock](/static/img/WOLReadMeOnestock.png)

### DataTables
![Data Table](/static/img/WOLReadMeDatatable.png)

### Installation

Clone or fork this repository:

```sh
$ git clone https://github.com/karenwsit/WOL
```
Create and activate a virtual environment inside the project directory:
```sh
$ cd WOL
$ virtualenv env
$ source env/bin/activate
```
Install the requirements:
```sh
$ pip install -r requirements.txt
```
In the WOL directory, type this command to start the server:
```
$ python server.py
Navigate your web browser to http://localhost:5000
