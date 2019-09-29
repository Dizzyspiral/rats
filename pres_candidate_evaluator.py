import sys
import json
import os
import glob
import re
from collections import defaultdict

import tweet_classifier
import evaluate_results

# Eventually, we should remove num_candidates and just detect it from the contents of the tweet directory
num_hours = 24 # 24 hours worth of tweets
num_candidates = 4 # number of candidates being tracked

def get_most_recent_filenames(directory, num_files):
    """
    Gets num_files number of recent files' names from directory, sorts the 
    names by file modified time, and returns them
    """
    files = list(filter(os.path.isfile, glob.glob(directory + os.sep + "*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    
    # XXX Hack: we don't want to include the most recent hour, as we're still 
    # scraping tweets for it. So we adjust the slicing. This function doesn't 
    # really do what it's described to. Probably we should post-process the 
    # value returned from it instead of hamfisting this in here.
    slice_begin = 0 - num_files - num_candidates
    slice_end = 0 - num_candidates
    recent = files[slice_begin:slice_end]

    return recent

def build_xaxis_labels(tweet_filenames):
    """
    Creates and returns a list of x-axis labels for a chart of tweet sentiment 
    results
    """
    labels = []

    for i in range(0, len(tweet_filenames), num_candidates):
        f = tweet_filenames[i]
        matches = re.search("(\d+-\d+-\d\d\d\d)_(\d+)", f)
        label = matches.group(1) + " " + matches.group(2) + ":00"
        labels.append(label)

    return labels

# Maybe move this to extract_tweet_text.py
def get_tweets_from_file(tweet_filename):
    """
    Returns a list of tweet texts extracted from tweets in tweet_filename
    """
    tweets = []

    with open(tweet_filename, 'r') as f:
        for raw_tweet in f:
            tweet = json.loads(raw_tweet)
            tweets.append(tweet["text"])

    return tweets

def get_class_labels_from_file(f):
    tweets = get_tweets_from_file(f)
    results = []

    for t in tweets:
        results.append(tweet_classifier.classify_tweet_text(t))
    
    return results
    
def get_percent_positive(results):
    percent_results = evaluate_results.calculate_percentages(results)
    return percent_results['pos']

def get_p_pos_from_file(f):
    r = get_class_labels_from_file(f)
    p = get_percent_positive(r)

    return p

def get_candidate_name(tweet_filename):
    """ Get a candidate's name from the tweet filename"""

    matches = re.search("\d+-\d+-\d\d\d\d_\d+_(\w+)", tweet_filename)
    name = matches.group(1)
    # This replaces underscores with spaces and capitalizes the parts of the name
    name = " ".join([x.capitalize() for x in name.split('_')])
    
    return name

def build_results(tweet_filenames):
    results = defaultdict(lambda: [])

    for f in tweet_filenames:
        candidate = get_candidate_name(f)
        results[candidate].append(get_p_pos_from_file(f))

    return results

def build_js_data(xlabels, results):
    """
    Creates the text of a javascript data file that can be used by the 
    presiment project to display a chart/graph of the candidate sentiment
    data
    """
    # Eventually we'll make this build the JS in a loop without assuming who the 
    # candidates are. But that's going to require reworking the template to also
    # generate the chart style. This is just lazy and easy for now.
    js = "var biden_data = " + str(results['Joe Biden']) + ";\n"
    js += "var bernie_data = " + str(results['Bernie Sanders']) + ";\n"
    js += "var trump_data = " + str(results['Donald Trump']) + ";\n"
    js += "var warren_data = " + str(results['Elizabeth Warren']) + ";\n"
    js += "var xlabels = " + str(xlabels) + ";\n"

    return js

def print_usage():
    """Prints out how to use this script"""
    print(sys.argv[0] + " classifier_pickle tweets_directory")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        exit()

    classifier_pickle = sys.argv[1]
    tweets_dir = sys.argv[2]

    tweet_classifier.load_classifier(classifier_pickle)
    tweet_filenames = get_most_recent_filenames(tweets_dir, num_hours * num_candidates)
    xlabels = build_xaxis_labels(tweet_filenames)
    print(xlabels)
    results = build_results(tweet_filenames)
    print(results)
    js = build_js_data(xlabels, results)

    with open('data.js', 'w') as f:
        f.write(js)
