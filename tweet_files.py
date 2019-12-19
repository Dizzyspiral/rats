import threading
import json
import datetime
import os

class HourlyTweetFile():
    def __init__(self, basename, directory):
        self.file_lock = threading.Lock()
        self.basename = basename
        self.directory = directory
        self.update_file_handle()

    def make_filename(self):
        now = datetime.datetime.now()
        return "%s%s%d-%d-%d_%d_%s" % (self.directory, os.sep, now.month, now.day, now.year, now.hour, self.basename)

    def update_file_handle(self):
        print("[HourlyTweetFile] Updating file handle")
        filename = self.make_filename()
        self.file_lock.acquire()

        try:
            self.filehandle = open(filename, 'a', encoding='utf-8')
        except:
            print("Error opening new file '%s'" % filename)
        finally:
            self.file_lock.release()

    def write_tweet(self, tweet):
        self.file_lock.acquire()

        try:
            self.filehandle.write(json.dumps(tweet))
            self.filehandle.write('\n')
        except:
            print("Error writing tweet to output file")
        finally:
            self.file_lock.release()

class MinuteTweetFile():
    def __init__(self, basename, directory):
        self.file_lock = threading.Lock()
        self.basename = basename
        self.directory = directory
        self.update_file_handle()

    def make_filename(self):
        now = datetime.datetime.now()
        return "%s%s%d-%d-%d_%d_%d_%s" % (self.directory, os.sep, now.month, now.day, now.year, now.hour, now.minute, self.basename)

    def update_file_handle(self):
        print("[MinuteTweetFile] Updating file handle")
        filename = self.make_filename()
        self.file_lock.acquire()

        try:
            self.filehandle = open(filename, 'a', encoding='utf-8')
        except:
            print("Error opening new file '%s'" % filename)
        finally:
            self.file_lock.release()

    def write_tweet(self, tweet):
        self.file_lock.acquire()

        try:
            self.filehandle.write(json.dumps(tweet))
            self.filehandle.write('\n')
        except:
            print("Error writing tweet to output file")
        finally:
            self.file_lock.release()
