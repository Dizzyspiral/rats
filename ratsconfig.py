import os

CONSUMER_KEY = os.getenv("RATS_CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("RATS_CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("RATS_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("RATS_ACCESS_TOKEN_SECRET", None)

# Eventually add @POTUS
FOLLOW = ['@realDonaldTrump']
#FOLLOW = ['@HillaryClinton']

#USERS = ['@realDonaldTrump',
#         '@HillaryClinton']
#TAGS = ['#debates', '#debatenight', '#decision2016']
#FOLLOW = ['@realDonaldTrump', '@HillaryClinton', '#debate', '#debates', '#debatenight', '#decision2016', 'debate', 'debates', '#WomenForTrump', '#MAGA', '#Trump2016', '#TeamTrump', '#TrumpPence16', '#MakeAmericaGreatAgain', '#TrumpTrain', '#AmericaFirst', '#VoteTrump', '#MoreQualifiedThanTrump', '#StopTrump', '#NeverTrump', '#drumpf', '#dumptrump', '#ImWithHer', '#Hillary2016', '#strongertogether', '#LoveTrumpsHate', '#OhHillYes', '#WhyImWithHer', '#YesWeKaine', '#HillYes', '#VoteHillary', '#Shillary', '#NeverHillary', '#crookedhillary']

