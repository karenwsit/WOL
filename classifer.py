from nltk.classify import NaiveBayesClassifier
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
import nltk.classify.util
import re
import csv
import random

"""
Training & Testing NaiveBayesClassifier

"""

test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]


def read_file():
    with open('small_training.csv', 'r') as f:
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


if __name__ == "__main__":
	raw_training_tweets = read_file()
	training_tweets = clean_tweets(raw_training_tweets)
	print training_tweets
	print "***************************************************************"

	# split cleaned tweet list into test and training
	# small_training_tweets = random.sample(range(len(training_tweets)), .75*len(training_tweets))
	# small_test_tweets = int(len(tweet_list) * 0.75)

	training_set = nltk.classify.apply_features(extract_features, training_tweets) 
	test_set = nltk.classify.apply_features(extract_features, test_tweets)

	classifier = nltk.NaiveBayesClassifier.train(training_set)

	# print 'accuracy:', nltk.classify.accuracy(classifier, test_set)
	# print classifier.show_most_informative_features()


# dist = classifier.prob_classify(features)
# for label in dist.samples():
#     print("%s: %f" % (label, dist.prob(label)))

# classifier.classify(extract_features(tweet.split()))
# classifier_object = classifier.prob_classify(extract_features(tweet.split()))
# classifier_object.logprob('positive')
# classified_object.logprob('negative')

# print 'precision:', nltk.metrics
