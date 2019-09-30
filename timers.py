import datetime
import threading
import time

class HourlyTimer(threading.Thread):
    def __init__(self, callbacks):
        threading.Thread.__init__(self)
        self.callbacks = callbacks

    def run(self):
        while(True):
            self.detect_hour_change()
            self.execute_callbacks()

    def detect_hour_change(self):
        """ Watches the current time to see when the hour changes """
        prev_hour = datetime.datetime.now().hour

        while prev_hour == datetime.datetime.now().hour:
            time.sleep(0) # Yield execution to another thread

        # We get here once the hour has changed
        return True

    def execute_callbacks(self):
        print("[HourlyTimer] Executing callbacks")
        for callback in self.callbacks:
            callback()