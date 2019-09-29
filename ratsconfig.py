import os

CONSUMER_KEY = os.getenv("RATS_CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("RATS_CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("RATS_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("RATS_ACCESS_TOKEN_SECRET", None)
TAGFILE = "tags.txt"

def get_tags():
    tags = []

    try:
        with open(TAGFILE) as f:
           for word in f.read().split():
                tags.append(word)
    except:
        # If TAGFILE does not exist or cannot be read, we give tags 
        # an invalid value, so that other modules which use this can 
        # detect it and handle the error how they'd like.
        tags = None

    return tags 

FOLLOW = get_tags()

