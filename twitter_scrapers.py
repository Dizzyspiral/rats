import sys
import json
import threading

from twitter import Api
import ratsconfig

api = Api(ratsconfig.CONSUMER_KEY,
          ratsconfig.CONSUMER_SECRET,
          ratsconfig.ACCESS_TOKEN,
          ratsconfig.ACCESS_TOKEN_SECRET)

class SubstreamScraper(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.substreams = []
        self.tags = []

    def add_substream(self, tags, callback):
        self.substreams.append([tags, callback])
        self.tags.extend(tags)

    def run(self):
        for tweet in api.GetStreamFilter(track=self.tags):
            raw_tweet = json.dumps(tweet)
            for tags, callback in self.substreams:
                for tag in tags:
                    if raw_tweet.find(tag) != -1:
                        callback(tweet)
                        break

class Scraper(threading.Thread):
    def __init__(self, tags, callback):
        threading.Thread.__init(self)
        self.tags = tags
        self.callback = callback

    def run(self):
        for line in api.GetStreamFilter(track=self.tags):
            self.callback(line)
