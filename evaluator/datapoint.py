import pickle
import re

import tweeteval

class DataPoint:
    def __init__(self, filename, class_pickle):
        self.filename = filename
        self.candidate = self._build_candidate_name()
        self.xlabel = self._build_xlabel()
        self.classifier_pickle = class_pickle
        self.value = self._build_value()

    def __lt__(self, other):
        print("Called __lt__")
        return self.get_date_int() < other.get_date_int() 

    def _adjust_digits(self, s, digits):
        diff = digits - len(s)
        
        if diff > 0:
            for i in xrange(diff):
                s = "0" + s
            
        return s

    def get_date_int(self):
        matches = re.search("(\d+)-(\d+)-(\d\d\d\d)_(\d+)_(\d+)", self.filename)
        month = str(matches.group(1))
        day = str(matches.group(2))
        year = str(matches.group(3))
        hour = str(matches.group(4))
        minute = str(matches.group(5))

        year = self._adjust_digits(year, 4)
        month = self._adjust_digits(month, 2)
        day = self._adjust_digits(day, 2)
        hour = self._adjust_digits(hour, 2)
        minute = self._adjust_digits(minute, 2)

        result = year + month + day + hour + minute

        return int(result)

    def _load_classifier(self, pickle_file):
        """
        Loads a tweet classifier to use when classifying tweets.
        """
        return pickle.load(open(pickle_file, 'rb'))

    def _build_xlabel(self):
        matches = re.search("(\d+-\d+-\d\d\d\d)_(\d+)", self.filename)
        return matches.group(1) + " " + matches.group(2) + ":00"

    def _build_candidate_name(self):
        """ Get a candidate's name from the tweet filename"""
        matches = re.search("\d+-\d+-\d\d\d\d_\d+_(\w+)", self.filename)
        name = matches.group(1)
        # This replaces underscores with spaces and capitalizes the parts of the name
        name = " ".join([x.capitalize() for x in name.split('_')])

        return name

    def _build_value(self):
        classifier = self._load_classifier(self.classifier_pickle)
        results = tweeteval.classify_tweet_file(self.filename, classifier)
        percents = tweeteval.interpret_results(results)

        return percents['pos'] * 100
