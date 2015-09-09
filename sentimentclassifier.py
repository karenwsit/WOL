from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
import re
import csv
from models.model import User, Stock, UserStock, TwitterHandle, Tweet, Sentiment, connect_to_db, db

"""
Training & Testing NaiveBayesClassifier

"""

def read_file():
    with open('1.6milliontrainingtweets.csv', 'r') as f:
    	tweet_list = []
        for row in csv.reader(f.read().splitlines()):
	    	tweet = row[5] 
	    	tweet1 = re.sub(r"http\S+", "", tweet)
	    	clean_tweet2 = re.sub(r"@\S+", "", tweet1).replace('"','').replace(',','').replace('.','').strip().split("\n")
	    	if int(row[0]) == 0:
	    		tweet_tuple = (clean_tweet2[0],'negative')
	    	elif int(row[0]) == 4:
	    		tweet_tuple = (clean_tweet2[0],'positive')
	    	tweet_list.append(tweet_tuple)
    return tweet_list

def clean_tweets(tweet_list):
	tweet_words = []
	for (words, sentiment) in tweet_list:
		words_filtered = [w.lower() for w in words.split() if len(w) >=3]
		tweet_words.append((words_filtered, sentiment))
	return tweet_words

#creating a feature extractor dictionary to decide relevant features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in document_words:
		features['contains(%s)' % word] = (word in document_words)
	return features

def get_trained_classifier():
	raw_training_tweets = read_file()
	training_tweets = clean_tweets(raw_training_tweets)
	training_set = nltk.classify.apply_features(extract_features, training_tweets) 
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	return classifier
	

if __name__ == "__main__":
	get_trained_classifier()
