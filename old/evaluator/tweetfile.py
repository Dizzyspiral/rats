import json

def get_tweets(filename):
    tweets = []

    with open(filename, 'r') as f:
        for tweet in f:
            tweet = json.loads(tweet)

            try:
                text = tweet["full_text"]
            except:
                text = tweet["text"]

            tweets.append(text)

    return tweets
