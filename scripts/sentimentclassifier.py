import time
import nltk.classify.util
import re
import csv
import pickle
import os.path

"""
Training & Testing NaiveBayesClassifier

"""
word_features = None


def split_training_file():
    save_path = '/Users/karensit/src/HB_Project/csv_files'
    output_base = 'output'
    at = 5000
    split_len = 5000

    big_file = open('10KTweets.csv', 'r')
    split_file = big_file.read().splitlines()
    for lines in range(0, len(split_file), split_len):
        output_data = split_file[lines:lines+split_len]
        complete_name = os.path.join(save_path, output_base + str(at) + ".csv")
        output = open(complete_name, 'w')
        output.write('\n'.join(output_data))
        output.close()
        at += 5000
    return


def read_file(small_file):
    with open('small_file', 'r') as f:
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
    global word_features
    word_features = word_list.keys()
    return word_features


def create_extract_features_dict(document):
    document_words = set(document)
    features = {}
    global word_features
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def get_trained_classifier():
    split_training_file()
    # for file_name in os.listdir('.'):
    #     if os.path.isfile(file_name):

    raw_training_tweets = read_file()
    training_tweets = tokenize_tweets(raw_training_tweets)
    word_features = create_word_features(training_tweets)
    training_set = nltk.classify.apply_features(create_extract_features_dict, training_tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier



if __name__ == "__main__":
    start = time.clock()
    # get_trained_classifier()
    split_training_file()
    duration = (time.clock() - start)*1000
    print "TIME IT TAKES TO RUN THIS FILE: %f" % (duration)
