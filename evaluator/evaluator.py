import sys
import os
from datetime import datetime
#from mem_top import mem_top # Debugging memory leak

import tweetdir
from datapoint import DataPoint
import jsbuilder

def print_usage():
    print(sys.argv[0] + " num_hours num_candidates tweet_dir classifier_pickle js_outfile")

def get_datapoints(tweet_files):
    datapoints = []

    for f in tweet_files:
#        print("[Main] ---memtop---\n")
#        print(mem_top())
        print("[Main] processing '" + f)
        datapoints.append(DataPoint(f, class_pickle))

    return datapoints

def write_js(datapoints):
    js = jsbuilder.build_js(datapoints)

    with open(jsfile, 'w') as f:
        f.write(js)

def archive_tweet_files(tweet_dir, tweet_files):
    print("[Main] Archiving...")
    cur_time = datetime.now()
    archive_file = "archive_" + cur_time.year + "-" + cur_time.month + "-" + cur_time.day + "_" + cur_time.hour + "_" + cur_time.minute + ".tgz"
    os.system("tar -czvf" + archive_file + " " + " ".join(tweet_files))

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
    datapoints.extend(get_datapoints(tweet_files))
    write_js(datapoints)
    archive_tweet_files(tweet_dir, tweet_files)
    # Wait for minute to change, and do it again

