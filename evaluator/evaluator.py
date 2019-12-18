import sys

import tweetdir
from datapoint import DataPoint
import jsbuilder

def print_usage():
    print(sys.argv[0] + " num_hours num_candidates tweet_dir classifier_pickle js_outfile")

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print_usage()
        exit()

    num_hours = int(sys.argv[1])
    num_candidates = int(sys.argv[2])
    tweet_dir = sys.argv[3]
    class_pickle = sys.argv[4]
    jsfile = sys.argv[5]
    datapoints = []

    tweet_files = tweetdir.get_recent_files(tweet_dir, num_hours, num_candidates)
    
    for f in tweet_files:
        print("[Main] processing '" + f + "'...")
        datapoints.append(DataPoint(f, class_pickle))

    js = jsbuilder.build_js(datapoints)

    with open(jsfile, 'w') as f:
        f.write(js)
