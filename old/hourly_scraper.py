import datetime
import threading
import json
from time import sleep
from twitter import Api

import ratsconfig

api = Api(ratsconfig.CONSUMER_KEY,
          ratsconfig.CONSUMER_SECRET,
          ratsconfig.ACCESS_TOKEN,
          ratsconfig.ACCESS_TOKEN_SECRET)

# This is updated by update_file_handle, so that the write location for the 
# tweets changes transparent to the scraping thread
filehandle = None

# Locks the file for writing while the handle is being changed
outfile_lock = threading.Lock()

class TimerThread(threading.Thread):
    def __init__(self, basename):
        threading.Thread.__init__(self)
        self.basename = basename

    def run(self):
        while(True):
            self.update_file_handle()
            self.detect_hour_change()

    def update_file_handle(self):
        global filehandle

        hourfile = self.make_filename()
        outfile_lock.acquire()

        try:
            filehandle = open(hourfile, 'a')
        except:
            print("Error opening new file '%s'" % hourfile)
        finally:
            outfile_lock.release()

    def make_filename(self):
        now = datetime.datetime.now()
        return "%d-%d-%d_%d_%s" % (now.month, now.day, now.year, now.hour, self.basename)

    def detect_hour_change(self):
        """ Watches the current time to see when the hour changes """
        prev_hour = datetime.datetime.now().hour
        
        while prev_hour == datetime.datetime.now().hour:
            sleep(0) # Yield execution to another thread

        # We get here once the hour has changed
        return True

def scrape_tweets(tags, basefile):
    """
    Loops forever getting tweets for the specified tags. The output file name 
    is dynamically generated based on the date and time, but includes the 
    basename as a differentiator. The output file name changes every hour such 
    that each hour's tweets are stored in separate files.
    """
    timerthread = TimerThread(basefile)
    timerthread.start()

    while(True):
        for line in api.GetStreamFilter(track=tags):
            outfile_lock.acquire()
            try:
                filehandle.write(json.dumps(line))
                filehandle.write('\n')
            except:
                print("Error writing tweet to output file")
            finally:
                outfile_lock.release()

if __name__ == '__main__':
    scrape_tweets(['@realDonaldTrump'], 'trump.json')
