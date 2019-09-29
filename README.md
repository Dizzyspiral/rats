# Real-time Analysis of Twitter Sentiment (RATS)
Real-time Analysis of Twitter Sentiment (RATS) is a project that analyzes the sentiment of twitter data scraped from configurable tag sets.
For more information on the twitter scraper, see below.

The text of these tweets is analyzed for sentiment using a model trained on NLTK data.
The current effort is utilizing [nltk-trainer](https://github.com/japerk/nltk-trainer) in conjunction with the freely available [nltk corpora](http://www.nltk.org/data.html).

RATS is tested with Python 3.4, but will probably work with any version of Python 3.

## Installation and use
The following sections explain how to reproduce my results and start evaluating your own sets of scraped tweets for sentiment. 

### Prerequisites
We need `nltk` to train and use our classifier, and we need `python-twitter` to scrape twitter.
We're also going to need numpy, as it's a dependency of the trainer.
Install them by running these commands:

```
pip install nltk
pip install python-twitter
pip install numpy
```

Note that the `python-twitter` package is NOT the same as the `twitter` package.
If you're getting weird errors when you go to run the scraper, make sure you have the right one installed.

Next, to train the classifier, we need `nltk-trainer`.
Clone the repo somewhere.

```
git clone https://github.com/japerk/nltk-trainer
```

Finally, you'll also need twitter access tokens.
Anyone can get access tokens by "creating" a twitter app - you can find details in [the twitter developer docs](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html).
RATS reads the access tokens from your environment.
For convenience, I recommend making a bash script something like the following, which you can source to export the environment variables.
Alternatively you can add them to your bashrc, or any number of other things - just make sure they're in your environment when you go to run the scraper.

```
export RATS_CONSUMER_KEY="your consumer key here"
export RATS_CONSUMER_SECRET="your consumer secret here"
export RATS_ACCESS_TOKEN="your access token here"
export RATS_ACCESS_TOKEN_SECRET="your access token secret here"
```

### Train the base classifier
To classify tweets, you'll need to train the base classifier on the NLTK `twitter_samples` corpus.
You'll also need the `stopwords` corpus for effective text training.
To download those, run the 

```
python
import nltk
nltk.download('stopwords')
nltk.download('twitter_samples')
exit()
```

This should download the corpora to some central location.
If you're using Linux, this is `~/nltk_data/corpora`.
If Windows, I don't know - but it should have told you where it put them when you ran the above commands.

The corpus of tweets is divided into negative and positive samples, one file for each.
Each file (`negative_tweets.json` and `positive_tweets.json`) is a JSON dump of a ton of tweets.
We just want the text of the tweets, and we'd like them to be separated out in a way that a classifier can make sense of.
So what we're going to do is parse these two files into individual files that each contain one tweet's text.
In order to keep the positive and negative tweets separate, we'll dump them into different directories.

Run the following commands wherever you'd like the data to go:

```
mkdir train
mkdir train/neg
mkdir train/pos
```

You should end up with a directory structure like this:

```
train
├── neg
└── pos
```

Now run the RATS script to extract the tweets into the directories (note that this script requires Python 3):

```
python3 extract_tweet_text.py train/pos ~/nltk_data/corpora/twitter_samples/positive_tweets.json
python3 extract_tweet_text.py train/neg ~/nltk_data/corpora/twitter_samples/negative_tweets.json
```

Your training directories should now be full of equal amounts of tweets.

Now that our training data is properly preprocessed, we can train our classifier.
Switch to whatever directory you checked out [`nltk-trainer`](https://github.com/japerk/nltk-trainer) to, and run the following command (adjusting for the location of your training data):

```
python train_classifier.py path-to-training-data/train/ --instances files --classifier NaiveBayes
```

If it worked correctly, you should see something like the following:

```
loading ../twitterfingers/rats/train/
2 labels: ['neg', 'pos']
using bag of words feature extraction
10000 training feats, 10000 testing feats
training NaiveBayes classifier
accuracy: 0.953700
neg precision: 0.948941
neg recall: 0.959000
neg f-measure: 0.953944
pos precision: 0.958561
pos recall: 0.948400
pos f-measure: 0.953453
dumping NaiveBayesClassifier to /home/dizzyspiral/nltk_data/classifiers/train_NaiveBayes.pickle
```

If it didn't work, make sure you have numpy installed.
You might also need to try python2 instead of python3.

I'm not going to go into any detail on the classifier - but I highly recommend you learn how it works if you plan on tweaking the training data or using the classifier on unique data, as changing the parameters of a classifier can have drastic results.

Anyway, now your classifier is ready to use!

## Scraping tweets
The twitter scraper grabs tweets in real time filtered by a list of tags.
Tags can be `#hashtags`, `@mentions`, or just words that you'd like to see included in the tweet.
The scraper reads a list of space-separated tags out of `tags.txt` in the current directory.

Please recall that you need to have API access keys in order to use the scraper - see the prerequisites section, above, for more information.

Once you've configured your tags and have your keys exported into your environment, simply run the scraper, supplying an output file to write to.

```
python twitter_scraper.py tweets.json
```

Depending on the tags you've selected, this file will get large, fast.
Make sure you have enough disk space to accommodate your collection.

## Classifying scraped tweets
Just like the training data, the scraped tweets all end up in one big JSON file.
To extract the tweets into a directory of tweet files suitable for classification, run the following commands:

```
mkdir somedir
python3 extract_tweet_text.py somedir tweets.json
```

Then, to classify your tweets, run:

```
python tweet_classifier.py ~/nltk_data/classifiers/train_NaiveBayes.pickle test/ test.class
```

This will dump the classification results for each tweet into a file, where each class label (neg or pos) is on its own line.
The `evaluate_results` script will print out a summary of the percentage of each label.

```
python evaluate_results.py test.class 
```

## Analyzing political data
This project began as an effort to quantify the country's sentiment toward each political candidate in the 2016 presidential election.
You'll have to take my word for it, but the wonderful thing is, it worked - even though half the country was shocked by the election of Donald Trump, the prevailing sentiment for Donald was far more positive than it was for Hillary.
My efforts for this project now continue to be politically based, in that I am attempting to track sentiments relating to US politicians for English-speaking populations both at home and abroad.
The reason that the experiments are limited to English-speakers is because the NLTK data I am using for training was exclusively English tweets.
If anyone can point me in the direction of a training data set for positive/negative sentiment for non-English languages, I would be very interested in incorporating it.

## Future work
Since this is a politically motivated project, it would likely improve the results for it to be trained on political tweets.
Creating a training set of political tweets for the classifier probably wouldn't be too hard.
The original dataset (`sample_tweets` from NLTK) gets positive samples by grabbing tweets with smiley emoji, and negative samples from tweets with frowning emoji.
Deciding what filters to apply to make the dataset sufficiently "political" is the more nuanced problem.
This is something I may try in the future.
If I do, I'll be sure to publish the dataset for public use.
