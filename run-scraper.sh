echo $$ > pid.txt

while true
do
    python scraper.py tweets.db training_NaiveBayes.pickle
done
