from nltk.classify import NaiveBayesClassifier
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
import nltk.classify.util
import re
# from nltk.corpus import movie_reviews

"""
Training & Testing NaiveBayesClassifier

"""


test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]

def read_file(filename):

    text_file = open(filename)
    return text_file.read()

negtweets = read_file("negtweets.txt")
postweets = read_file("postweets.txt")

#regex to remove url from tweets
nourl_negtweets = re.sub(r"http\S+", "", negtweets).replace('"','').replace(',','').replace('.','').strip().split("\n")
nourl_postweets = re.sub(r"http\S+", "", postweets).replace('"','').replace(',','').replace('.','').strip().split("\n")

#put clean negtweets into a tuple & list
negtweets_list = []
for t in nourl_negtweets:
	negtweet_tuple = (t ,'negative')
	negtweets_list.append(negtweet_tuple)

#put clean postweets into a tuple & list
postweets_list = []
for t in nourl_postweets:
	postweet_tuple = (t ,'positive')
	postweets_list.append(postweet_tuple)

#combine pos & neg tweets
tweets = []
for (words, sentiment) in negtweets_list + postweets_list:
	words_filtered = [w.lower() for w in words.split() if len(w) >=3]
	tweets.append((words_filtered, sentiment))

#list of word features extracted from tweets. list of distinct words ordered by frequency of appearance
def get_words_in_tweets(tweets):
	all_words =[]
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	freq_dist = nltk.FreqDist(wordlist)
	word_features = freq_dist.keys()
	return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

#creating a feature extractor dictionary to decide relevant features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

#create training set by apply the features to classifier & passing tweets list in
training_set = nltk.classify.apply_features(extract_features, tweets) 

#train the classifer
classifier = nltk.NaiveBayesClassifier.train(training_set)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, test_tweets)

classifier.classify(extract_features(tweet.split()))
classifier_object = classifier.prob_classify(extract_features(tweet.split()))
classifier_object.logprob('positive')
classified_object.logprob('negative')

print 'precision:', nltk.metrics


# def word_feats(words):
# 	return dict([(word, True) for word in words])

# negids = movie_reviews.fileids('neg')
# posids = movie_reviews.fileids('pos')

# negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
# posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# negcutoff = len(negfeats)*3/4
# poscutoff = len(posfeats)*3/4

# trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
# testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
# print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

# classifier = NaiveBayesClassifier.train(trainfeats)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()



