# Real-time Analysis of Twitter Sentiment (RATS)
Real-time Analysis of Twitter Sentiment (RATS) is a project that analyzes the sentiment of twitter data scraped from configurable tag sets.
For more information on the twitter scraper, see below.

The text of these tweets is analyzed for sentiment using a model trained on NLTK data.
The current effort is utilizing [nltk-trainer](https://github.com/japerk/nltk-trainer) in conjunction with the freely available [nltk corpora](http://www.nltk.org/data.html).

RATS is tested with Python 3.4, but will probably work with any version of Python 3.

## Twitter scraper
The twitter scraper, `twitter_scraper.py`, is designed to download tweets and place them each in unique files.
Most of its features aren't implemented yet; currently, it just grabs tweets and prints them to an output file.
The script `extract_tweet_text.py` can be used on the output file to extract the text of each tweet and write them out to their own files.

## Tweet classifier
The script `tweet_classifier.py` takes as input a trained model (in the form of a `.pickle` file) and a tweet to classify.
It outputs the classification (pos or neg) of the tweet.

# How to analyze data
TODO: write up how to create a classifier using NLTK and NLTK-trainer, then use this classifier with the twitter data scripts contained in thie project to evaluate sentiment.

## Analyzing political data
This project began as an effort to quantify the country's sentiment toward each political candidate in the 2016 presidential election.
You'll have to take my word for it, but the wonderful thing is, it worked - even though half the country was shocked by the election of Donald Trump, the prevailing sentiment for Donald was far more positive than it was for Hillary.
My efforts for this project now continue to be politically based, in that I am attempting to track sentiments relating to US politicians for English-speaking populations both at home and abroad.
The reason that the experiments are limited to English-speakers is because the NLTK data I am using for training was exclusively English tweets.
If anyone can point me in the direction of a training data set for positive/negative sentiment for non-English languages, I would be very interested in incorporating it.
