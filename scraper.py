from twitter import Api
import sqlite3
import os
import sys
import datetime
import pickle
import json

# XXX TBD things to fix:
# - tweet table is hardcoded as a string in multiple places, not easy to change
# - schema is hard-coded in multiple places, not easy to change

FLAG_DEBUG = False

def configure_twitter():
    CONSUMER_KEY = os.getenv("RATS_CONSUMER_KEY", None)
    CONSUMER_SECRET = os.getenv("RATS_CONSUMER_SECRET", None)
    ACCESS_TOKEN = os.getenv("RATS_ACCESS_TOKEN", None)
    ACCESS_TOKEN_SECRET = os.getenv("RATS_ACCESS_TOKEN_SECRET", None)

    try:
        api = Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    except:
        print("Unable to configure twitter API, exiting.")

    return api

def table_exists(tablename, cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tweets'")
    result = cursor.fetchall()
    
    return len(result) > 0

def configure_sqlite(dbname):
    try:
        conn = sqlite3.connect(dbname)
    except:
        print("Unable to open Sqlite database '" + str(dbname) + "', exiting.")

    cursor = conn.cursor()

    # Check if table tweets already exists
    if not table_exists("tweets", cursor):
        # If not, create it
        cursor.execute("CREATE TABLE tweets (tag text, time text, classification text)")
        conn.commit()

    return conn

def configure_classifier(picklefile):
    classifier = pickle.load(open(picklefile, 'rb'))

    return classifier
 
def configure():
    api = configure_twitter()
    conn = configure_sqlite(sys.argv[1])
    classifier = configure_classifier(sys.argv[2])

    return api, conn, classifier

def classify_tweet(tweet, classifier):
    words = tweet.split()
    features = dict([(word, True) for word in words])
    ret = classifier.classify(features)

    return ret

def get_tweet_text(tweet):
    try:
        text = tweet["extended_tweet"]["full_text"]
    except:
        text = tweet["text"]

    return text

def get_tweet_time(tweet):
    tweet_time = tweet["created_at"]
    d = datetime.datetime.strptime(tweet_time, "%a %b %d %H:%M:%S +0000 %Y")

    return d.isoformat()

def debug_print(s):
    if FLAG_DEBUG:
        print(s)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: " + str(sys.argv[0]) + " sqlite_db classifier_pickle")
        sys.exit(0)

    debug_print("Configuring...")
    api, conn, classifier = configure()
    cursor = conn.cursor()
    debug_print("Configured successfully.")
    tags = ['@realDonaldTrump', '@POTUS', '@JoeBiden']
    then = datetime.datetime.now()

    debug_print("Starting scraper...")
    for tweet in api.GetStreamFilter(track=tags):
        raw_tweet = json.dumps(tweet)
        debug_print("Received tweet.")
       
        # Record the tweet once for each tag that applies to it 
        for tag in tags:
            if raw_tweet.find(tag) != -1:
                debug_print("Found tag for tweet")
                time = get_tweet_time(tweet)
                text = get_tweet_text(tweet)
                debug_print("Classifying tweet...")
                classification = classify_tweet(text, classifier)
                debug_print("Tweet successfully classified as '" + str(classification) + "'")
                debug_print("Adding tweet to database...")

                try:
                    cursor.execute("INSERT INTO tweets VALUES(?,?,?)", (tag, time, classification))
                    conn.commit()
                    debug_print("Tweet successfully added to database.")
                except:
                    print("Database busy (analysis is probably running). Skipping to next tweet")

        # Check time for hour change
        now = datetime.datetime.now()

        if now.hour != then.hour:
            conn.close()
            sys.exit(0)
