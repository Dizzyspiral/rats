import sys
import os
import datetime
import time
import subprocess
import tarfile
#from mem_top import mem_top # Debugging memory leak

import tweetdir
from datapoint import DataPoint
import jsbuilder

def print_usage():
    print(sys.argv[0] + " num_minutes num_candidates tweet_dir classifier_pickle js_outfile")

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
    cur_time = datetime.datetime.now()
    archive_file = "archive_" + str(cur_time.year) + "-" + str(cur_time.month) + "-" + str(cur_time.day) + "_" + str(cur_time.hour) + "_" + str(cur_time.minute) + ".tgz"

    with tarfile.open(archive_file, 'w:xz') as t:
        for f in tweet_files:
            t.add(f)

    cmd = ["rm"]
    cmd = cmd.extend(tweet_files)
    print(cmd)
    subprocess.check_call(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print_usage()
        exit()

    num_minutes = int(sys.argv[1])
    num_candidates = int(sys.argv[2])
    tweet_dir = sys.argv[3]
    class_pickle = sys.argv[4]
    jsfile = sys.argv[5]
    datapoints = []

    while True:
        prev_minute = datetime.datetime.now().minute
        tweet_files = tweetdir.get_recent_files(tweet_dir, num_minutes, num_candidates)
        datapoints.extend(get_datapoints(tweet_files))
        write_js(datapoints)
        archive_tweet_files(tweet_dir, tweet_files)
        
        # Wait for minute to change, and do it again
#        while prev_minute == datetime.datetime.now().minute:
#            time.sleep(1)

