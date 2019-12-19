import threading
import time

from twitter_scrapers import SubstreamScraper
from tweet_files import HourlyTweetFile
from timers import HourlyTimer
from tweet_files import MinuteTweetFile
from timers import MinuteTimer

candidates = {
#        'michael_bennet': ['@MichaelBennet', '@SenatorBennet'],
        'joe_biden': ['@JoeBiden'],
#        'bill_de_blasio': ['@billdeBlasio', '@NYCMayor'],
#        'cory_booker': ['@CoryBooker', '@CoryABooker2020', '@SenBooker'],
#        'steve_bullock': ['@GovernorBullock'],
        'pete_buttigieg': ['@PeteButtigieg'],
        'julian_castro': ['@JulianCastro'],
#        'john_delaney': ['@JohnDelaney'],
#        'tulsi_gabbard': ['@TulsiGabbard', '@TulsiPresident'],
#        'kirsten_gillibrand': ['@SenGillibrand', '@gillibrandny'],
#        'mike_gravel': ['@MikeGravel'],
#        'kamala_harris': ['@KamalaHarris','@SenKamalaHarris'],
#        'john_hickenlooper': ['@Hickenlooper'],
#        'jay_inslee': ['@JayInslee', '@GovInslee'],
        'amy_klobuchar': ['@amyklobuchar', '@SenAmyKlobuchar'],
#        'wayne_messam': ['@WayneMessam'],
#        'seth_moulton': ['@sethmoulton', '@teammoulton'],
#        'beto_orourke': ['@BetoORourke', '@RepBetoORourke'],
#        'tim_ryan': ['@TimRyan', '@RepTimRyan'],
        'bernie_sanders': ['@SenSanders', '@BernieSanders', '@TheBern2020'],
#        'eric_swalwell': ['@RepSwalwell', '@ericswalwell'],
        'donald_trump': ['@realDonaldTrump', '@POTUS'],
        'elizabeth_warren': ['@SenWarren', '@ewarren'],
#        'bill_weld': ['@GovBillWeld'],
#        'marianne_williamson': ['@marwilliamson'],
        'andrew_yang': ['@AndrewYang'],
}

# Sigh... global variable. Might be able to fix this, easy hack for now.
scraper = None

def print_art():
    print("""  ___________                                              
 /   _____/  | ______________  ___.__.______   ___________ 
 \_____  \|  |/ /\_  __ \__  \<   |  |\____ \_/ __ \_  __ \\
 /        \    <  |  | \// __ \\\\___  ||  |_> >  ___/|  | \/
/_______  /__|_ \ |__|  (____  / ____||   __/ \___  >__|   
        \/     \/            \/\/     |__|        \/       \n""")

def create_scraper():
    global scraper

    scraper = SubstreamScraper()
    tweet_files = []

    for candidate, tags in candidates.items():
        print("[Main] Making scraper thread for '%s', '%s'" % (candidate, tags))
#        tweet_files.append(HourlyTweetFile(candidate + '.json', 'tweets'))
        tweet_files.append(MinuteTweetFile(candidate + '.json', 'tweets'))
        scraper.add_substream(tags, lambda tweet, tf=tweet_files[-1]: tf.write_tweet(tweet))

    scraper.start()
   
def restart_scraper():
    global scraper

    scraper.force_exit = True
    scraper.join()
    create_scraper()
    print("[Main] Successfully restarted scraper")

if __name__ == '__main__':
    print_art()
    create_scraper()

#    timer = HourlyTimer([lambda: restart_scraper()])
    timer = MinuteTimer([lambda: restart_scraper()])
    timer.start()
    timer.join()

    # We shouldn't ever get here
    print("[Main] Exiting")
