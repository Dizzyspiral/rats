# Author: Dizzyspiral
# Purpose: transform the twitter_samples data into something that can be 
# classified by the nltk-classifier. We're only interested in the text
# field of the JSON that makes up the tweets, so we want to read each 
# tweet in, get the text field, and output it to a unique filename. We
# want the output format to be identical to what will come out of the 
# twitter-scraper.
# 
# Requires python 3

import json
import sys
import os

tweet_basename = "tweet_"
file_extension = ".txt"

def main():
    if (len(sys.argv) < 3):
        print("Usage: " + str(sys.argv[0]) + " output-dir path-to-twitter-corpus")
        exit()

    output_dir = sys.argv[1]
    tweet_count = 0

    with open(sys.argv[2]) as tweets_file:
        for raw_tweet in tweets_file:
            tweet_count += 1
            tweet = json.loads(raw_tweet)

            with open(output_dir + os.sep + tweet_basename + str(tweet_count) + file_extension, 'wt', encoding='utf-8') as output_file:
                output_file.write(tweet["text"])

if __name__ == '__main__':
    main()