import pickle
import sys
import os
from collections import defaultdict

import tweetfile

def load_classifier(pickle_file):
    """
    Loads a tweet classifier to use when classifying tweets. All classification 
    functions in this module will use this classifier.
    """
    global classifier
    classifier = pickle.load(open(pickle_file, 'rb'))

def classify_tweet(tweet, classifier):
    """ Classifies a tweet as either negative sentiment or positive sentiment """
    if classifier == None:
        print("Load a classifier before calling classify_tweet_text")
        return

    words = tweet.split()
    features = dict([(word, True) for word in words])
    ret = classifier.classify(features)

    return ret

def classify_tweet_file(filename, classifier):
    """ Classifies all tweets in a file, returning a list of results """
    results = []
    tweets = tweetfile.get_tweets(filename)

    for tweet in tweets:
        results.append(classify_tweet(tweet, classifier))

    return results

def interpret_results(results):
    """
    Interprets a list of results into percentages of positive and negative 
    sentiment
    """
    percentages = defaultdict(lambda: 0)

    # Accumulate the number of results of a particular type
    for result in results:
        percentages[result] += 1

    for label, value in percentages.items():
        percentages[label] = float(value) / float(len(results))

    return percentages



