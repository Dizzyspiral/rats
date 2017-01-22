import os

CONSUMER_KEY = os.getenv("RATS_CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("RATS_CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("RATS_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("RATS_ACCESS_TOKEN_SECRET", None)
TAGFILE = "tags.txt"

def get_tags():
    tags = []

    with open(TAGFILE) as f:
       for word in f.read().split():
            tags.append(word)

    return tags 

FOLLOW = get_tags()

