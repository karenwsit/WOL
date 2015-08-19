from nltk.classify import NaiveBayesClassifier
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
import nltk.classify.util
import re
import csv

"""
Training & Testing NaiveBayesClassifier

"""

test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]


#FOR THE TEST FILE

def read_file():
    with open('trainingtweets.csv', 'r') as f:
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

# def read_file():

#     text_file = open('testtweets.csv')
#     csv_file = csv.reader(text_file)

#     tweet_list = []
#     for row in csv_file:
#     	row = row.rstrip()
#     	tweet = row[5] 
#     	tweet1 = re.sub(r"http\S+", "", tweet)
#     	clean_tweet2 = re.sub(r"@\S+", "", tweet1).replace('"','').replace(',','').replace('.','').strip().split("\n")
#     	if int(row[0]) == 0:
#     		tweet_tuple = (clean_tweet2[0],'negative')
#     	elif int(row[0]) == 4:
#     		tweet_tuple = (clean_tweet2[0],'positive')
#     	tweet_list.append(tweet_tuple)
#     return tweet_list

def clean_tweets(tweet_list):
	tweet_words = []
	for (words, sentiment) in tweet_list:
		words_filtered = [w.lower() for w in words.split() if len(w) >=3]
		tweet_words.append((words_filtered, sentiment))
	return tweet_words

#list of word features extracted from tweets. list of distinct words ordered by frequency of appearance
def get_words_in_tweets(tweet_words):
	all_words =[]
	for (words, sentiment) in tweet_words:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	freq_dist = nltk.FreqDist(wordlist)
	word_features = freq_dist.keys()
	return word_features

# word_features = get_word_features(get_words_in_tweets(tweet_words))

#creating a feature extractor dictionary to decide relevant features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

#create training set by apply the features to classifier & passing tweets list in
def train_classifer(train_tweets, test_tweets, features_func=extract_features):
	training_set = nltk.classify.apply_features(features_func, train_tweets) 
	# print training_set

	#http://www.nltk.org/api/nltk.classify.html
	classifier = nltk.NaiveBayesClassifier.train(training_set)

	# exract features for test set, then run
	test_set = nltk.classify.apply_features(features_func, test_tweets) 

	print 'accuracy:', nltk.classify.accuracy(classifier, test_set)
	# classifier.show_most_informative_features()
	# print classifier.classify('Yo mama not working')



# dist = classifier.prob_classify(features)
# for label in dist.samples():
#     print("%s: %f" % (label, dist.prob(label)))

# classifier.classify(extract_features(tweet.split()))
# classifier_object = classifier.prob_classify(extract_features(tweet.split()))
# classifier_object.logprob('positive')
# classified_object.logprob('negative')

# print 'precision:', nltk.metrics


# trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
# testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
# print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

# classifier = NaiveBayesClassifier.train(trainfeats)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)



if __name__ == "__main__":
	tweet_list = read_file()
	real_cleaned_tweet_list = clean_tweets(tweet_list)
	cleaned_tweet_list = real_cleaned_tweet_list[:10]

	# split cleaned tweet list into test and training
	index_75percent = int(len(cleaned_tweet_list) * 0.75)
	# test_tweets = cleaned_tweet_list[index_75percent:]
	train_tweets = cleaned_tweet_list[:index_75percent]

	gotten_twitter_words = get_words_in_tweets(train_tweets)
	word_features = get_word_features(gotten_twitter_words)
	# print word_features

	extractor_dictionary = extract_features(word_features)
	# print extractor_dictionary

	# classifier = train_classifer(extractor_dictionary,cleaned_tweet_list)

	train_classifer(train_tweets, test_tweets)
	# print classifier

############################## OLD CODE ###########################
# negtweets = read_file("negtweets.txt")
# postweets = read_file("postweets.txt")

# #regex to remove url from tweets
# nourl_negtweets = re.sub(r"http\S+", "", negtweets).replace('"','').replace(',','').replace('.','').strip().split("\n")
# nourl_postweets = re.sub(r"http\S+", "", postweets).replace('"','').replace(',','').replace('.','').strip().split("\n")

# put clean negtweets into a tuple & list
# negtweets_list = []
# for t in nourl_negtweets:
# 	negtweet_tuple = (t ,'negative')
# 	negtweets_list.append(negtweet_tuple)

# #put clean postweets into a tuple & list
# postweets_list = []
# for t in nourl_postweets:
# 	postweet_tuple = (t ,'positive')
# 	postweets_list.append(postweet_tuple)


# def word_feats(words):
# 	return dict([(word, True) for word in words])

# negids = movie_reviews.fileids('neg')
# posids = movie_reviews.fileids('pos')

# negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
# posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# negcutoff = len(negfeats)*3/4
# poscutoff = len(posfeats)*3/4







