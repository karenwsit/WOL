import nltk.classify.util
import re
import csv

"""
Training & Testing NaiveBayesClassifier

"""
#global variable used in create_extract_features_dict; list of most frequent words in tweets
word_features = []


def read_file():
    with open('1.6milliontrainingtweets.csv', 'r') as f:
        tweet_list = []
        for row in csv.reader(f.read().splitlines()):
            tweet = row[5]
            tweet1 = re.sub(r"http\S+", "", tweet)
            clean_tweet2 = re.sub(r"@\S+", "", tweet1).replace('"', '').replace(',', '').replace('.', '').strip().split("\n")
            if int(row[0]) == 0:
                tweet_tuple = (clean_tweet2[0], 'negative')
            elif int(row[0]) == 4:
                tweet_tuple = (clean_tweet2[0], 'positive')
            tweet_list.append(tweet_tuple)
    return tweet_list


def tokenize_tweets(tweet_list):
    tweet_words = []
    for (words, sentiment) in tweet_list:
        words_filtered = [w.lower() for w in words.split() if len(w) >= 3]
        tweet_words.append((words_filtered, sentiment))
    return tweet_words


def create_word_features(tweet_words):
    all_words = []
    for (words, sentiment) in tweet_words:
        all_words.extend(words)
    word_list = nltk.FreqDist(all_words)
    word_features = word_list.keys()
    return word_features


def create_extract_features_dict(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def get_trained_classifier():
    raw_training_tweets = read_file()
    training_tweets = tokenize_tweets(raw_training_tweets)
    word_features = create_word_features(training_tweets)
    training_set = nltk.classify.apply_features(create_extract_features_dict, training_tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier


if __name__ == "__main__":
    get_trained_classifier()
