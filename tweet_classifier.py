import pickle
import sys

classifier = None

def load_classifier(pickle_file):
    global classifier
    classifier = pickle.load(open(pickle_file, 'rb'))

def classify_tweet(tweet_file):
    if classifier == None:
        print("Load a classifier before calling classify_tweet")
        return

    # Classify tweets
    with open(tweet_file, 'rb') as f:
        for line in f:
            words = line.split()
            features = dict([(word, True) for word in words])
            ret = classifier.classify(features)
            print(ret)

    # This just returns pos/neg. How do we get probabilities?
    return ret

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " pickle-file, tweet-file")
        exit()

    load_classifier(sys.argv[1])

    # Debugging an issue where everything seems to come out pos, and all the informative features are pos
    print(classifier.most_informative_features(100))

    classify_tweet(sys.argv[2])
