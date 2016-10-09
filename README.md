# Real-time Analysis of Twitter Sentiment (RATS)
Real-time Analysis of Twitter Sentiment (RATS) is a project that analyzes the sentiment of twitter data scraped from political streams.
Currently, the following streams are followed:

- Anything mentioning `@HillaryClinton`
- Anything mentioning `@realDonaldTrump`
- Anything mentioning `#debates`
- Anything mentioning `#debatenight`

For more information on the twitter scraper, see below.

The text of these tweets is analyzed for sentiment using a model trained on NLTK data.
The model is, currently, TBD, but the current effort is utilizing [nltk-trainer](https://github.com/japerk/nltk-trainer) in conjunction with the freely available [nltk corpora](http://www.nltk.org/data.html).

RATS is tested with Python 3.4, but will probably work with any version of Python 3.

## Twitter scraper
The twitter scraper, `twitter_scraper.py`, is designed to download tweets and place them each in unique files.
Most of its features aren't implemented yet; currently, it just grabs tweets and prints them to an output file.
The script `extract_tweet_text.py` can be used on the output file to extract the text of each tweet and write them out to their own files.

## Tweet classifier
The script `tweet_classifier.py` takes as input a trained model (in the form of a `.pickle` file) and a tweet to classify.
It outputs the classification (pos or neg) of the tweet.
