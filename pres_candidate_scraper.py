import threading
import time

import hourly_scraper

candidates = {
#        'michael_bennet': ['@MichaelBennet', '@SenatorBennet'],
        'joe_biden': ['biden', '@JoeBiden'],
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
        'beto_orourke': ['@BetoORourke', '@RepBetoORourke'],
#        'tim_ryan': ['@TimRyan', '@RepTimRyan'],
        'bernie_sanders': ['bernie', '@SenSanders', '@BernieSanders', '@TheBern2020'],
#        'eric_swalwell': ['@RepSwalwell', '@ericswalwell'],
        'donald_trump': ['@realDonaldTrump', '@POTUS', 'trump'],
        'elizabeth_warren': ['@SenWarren', '@ewarren'],
#        'bill_weld': ['@GovBillWeld'],
#        'marianne_williamson': ['@marwilliamson'],
#        'andrew_yang': ['@AndrewYang'],
}

class ScraperThread(threading.Thread):
    def __init__(self, tags, candidate):
        threading.Thread.__init__(self)
        self.tags = tags
        self.candidate = candidate
    
    def run(self):
        hourly_scraper.scrape_tweets(self.tags, self.candidate + ".json")

if __name__ == '__main__':
    for candidate, tags in candidates.items():
        print("Making scraper thread for '%s', '%s'" % (candidate, tags))
        thread = ScraperThread(tags, candidate)
        thread.start()
        # We sleep briefly so that twitter doesn't get all upset about us requesting a bunch of streams really quickly
        time.sleep(1) 
