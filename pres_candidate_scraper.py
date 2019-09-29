import threading
import time

from twitter_scrapers import SubstreamScraper
from tweet_files import HourlyTweetFile
from timers import HourlyTimer

candidates = {
#        'michael_bennet': ['@MichaelBennet', '@SenatorBennet'],
        'joe_biden': ['@JoeBiden'],
#        'bill_de_blasio': ['@billdeBlasio', '@NYCMayor'],
#        'cory_booker': ['@CoryBooker', '@CoryABooker2020', '@SenBooker'],
#        'steve_bullock': ['@GovernorBullock'],
#        'pete_buttigieg': ['@PeteButtigieg'],
#        'julian_castro': ['@JulianCastro'],
#        'john_delaney': ['@JohnDelaney'],
#        'tulsi_gabbard': ['@TulsiGabbard', '@TulsiPresident'],
#        'kirsten_gillibrand': ['@SenGillibrand', '@gillibrandny'],
#        'mike_gravel': ['@MikeGravel'],
#        'kamala_harris': ['@KamalaHarris','@SenKamalaHarris'],
#        'john_hickenlooper': ['@Hickenlooper'],
#        'jay_inslee': ['@JayInslee', '@GovInslee'],
#        'amy_klobuchar': ['@amyklobuchar', '@SenAmyKlobuchar'],
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
#        'andrew_yang': ['@AndrewYang'],
}

if __name__ == '__main__':
    scraper = SubstreamScraper()
    tweet_files = []
    timer_callbacks = []

    for candidate, tags in candidates.items():
        print("[Main] Making scraper thread for '%s', '%s'" % (candidate, tags))
        tweet_files.append(HourlyTweetFile(candidate + '.json', 'tweets'))
        scraper.add_substream(tags, lambda tweet, tf=tweet_files[-1]: tf.write_tweet(tweet))
        timer_callbacks.append(lambda tf=tweet_files[-1]: tf.update_file_handle())

    timer = HourlyTimer(timer_callbacks)
    scraper.start()
    timer.start()

