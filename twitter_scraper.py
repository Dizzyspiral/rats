import os
import json

from twitter import Api

CONSUMER_KEY = os.getenv("RATS_CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("RATS_CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("RATS_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("RATS_ACCESS_TOKEN_SECRET", None)

USERS = ['@realDonaldTrump',
         '@HillaryClinton']
TAGS = ['#debates', '#debatenight', '#decision2016']

api = Api(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_TOKEN_SECRET)

def main():
    with open('tweets.txt', 'a') as f:
        for line in api.GetStreamFilter(track=TAGS):
            f.write(json.dumps(line))
            f.write('\n')

if __name__ == '__main__':
    main()
