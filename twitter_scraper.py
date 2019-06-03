import sys
import json

from twitter import Api
import ratsconfig

api = Api(ratsconfig.CONSUMER_KEY,
          ratsconfig.CONSUMER_SECRET,
          ratsconfig.ACCESS_TOKEN,
          ratsconfig.ACCESS_TOKEN_SECRET)

def scrape_tweets(tags, outfile):
    with open(outfile, 'a') as f:
        for line in api.GetStreamFilter(track=tags):
            f.write(json.dumps(line))
            f.write('\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:" + sys.argv[0] + " output-file")
        exit()

    tags=ratsconfig.FOLLOW
    scrape_tweets(tags, sys.argv[1])
