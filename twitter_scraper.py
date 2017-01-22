import sys
import os
import json

from twitter import Api
import ratsconfig

api = Api(ratsconfig.CONSUMER_KEY,
          ratsconfig.CONSUMER_SECRET,
          ratsconfig.ACCESS_TOKEN,
          ratsconfig.ACCESS_TOKEN_SECRET)

def scrape_tweets():
    with open(sys.argv[1], 'a') as f:
        for line in api.GetStreamFilter(track=ratsconfig.FOLLOW):
            f.write(json.dumps(line))
            f.write('\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:" + sys.argv[0] + " output-file")
        exit()

    scrape_tweets()
