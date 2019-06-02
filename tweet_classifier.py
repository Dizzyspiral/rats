import pickle
import sys
import os

classifier = None

def load_classifier(pickle_file):
    global classifier
    classifier = pickle.load(open(pickle_file, 'rb'))

def classify_tweet(tweet_file):
    if classifier == None:
        print("Load a classifier before calling classify_tweet")
        return

    # In case the file has no lines, we create the variable here, to avoid unreferenced errors.
    ret = "Error"

    # Classify tweets
    with open(tweet_file, 'rt') as f:
        for line in f:
            words = line.split()
            features = dict([(word, True) for word in words])
            ret = classifier.classify(features)

    # This just returns pos/neg. How do we get probabilities?
    return ret

def classify_tweets(tweet_folder):
    results = []

    for tweet_file in os.listdir(tweet_folder):
        results.append(classify_tweet(tweet_folder + os.sep + tweet_file))

    return results

def write_multiple_results(results, results_file):
    with open(results_file, 'wt') as f:
        for result in results:
            f.write(result)
            f.write('\n')

def write_results(results, results_file):
    if hasattr(results, '__iter__'):
        write_multiple_results(results, results_file)
    else:
        with open(results_file, 'wt') as f:
            f.write(results)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: " + sys.argv[0] + " pickle-file tweet-file output-file")
        exit()

    load_classifier(sys.argv[1])

    if os.path.isdir(sys.argv[2]):
        results = classify_tweets(sys.argv[2])
    elif os.path.isfile(sys.argv[2]):
        results = classify_tweet(sys.argv[2])
    else:
        print("tweet-file must be a file or a directory")
        exit()

    write_results(results, sys.argv[3])
