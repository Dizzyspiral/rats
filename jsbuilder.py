import sqlite3
import datetime
from collections import defaultdict

def configure_sqlite(dbname):
    try:
        conn = sqlite3.connect("file:" + str(dbname) + "?mode=ro", uri=True)
    except:
        print("Unable to open Sqlite database '" + str(dbname) + "', exiting.")

    return conn

def get_min_max_times(conn):
    cursor = conn.cursor()
    min_row = cursor.execute("SELECT MIN(datetime(time)) FROM tweets")
    min_row = min_row.fetchone()[0]
    max_row = cursor.execute("SELECT MAX(datetime(time)) FROM tweets")
    max_row = max_row.fetchone()[0]
    
    min_time = datetime.datetime.strptime(min_row, "%Y-%m-%d %H:%M:%S")
    max_time = datetime.datetime.strptime(max_row, "%Y-%m-%d %H:%M:%S")

    return min_time, max_time

def get_percent_by_label(classifications):
    percentages = defaultdict(lambda: 0)

    for c in classifications:
        percentages[c] += 1

    for label, value in percentages.items():
        percentages[label] = float(value) / float(len(classifications))

    return percentages

def get_percent_pos(classifications):
    p = get_percent_by_label(classifications)
    
    return p['pos']

def get_datapoints(window_delta, dp_delta, conn):
    min_time, max_time = get_min_max_times(conn)

    trump_datapoints = []
    biden_datapoints = []
    labels = []
    trump_tags = ['@realDonaldTrump', '@POTUS']
    biden_tags = ['@JoeBiden']
    start_time = max_time - window_delta

    if start_time < min_time:
        start_time = min_time

    cur_time = start_time

    while cur_time + dp_delta < max_time:
        trump_classifications = []
        biden_classifications = []
        interval_start = cur_time
        interval_end = cur_time + dp_delta

        rows = cursor.execute("SELECT tag, classification, datetime(time) time FROM tweets WHERE time BETWEEN '" + interval_start.isoformat() + "' AND '" + interval_end.isoformat() + "'")
        results = rows.fetchall()

        for result in results:

            if result[0] in trump_tags:
                trump_classifications.append(result[1])
            if result[0] in biden_tags:
                biden_classifications.append(result[1])

        trump_datapoints.append(get_percent_pos(trump_classifications))
        biden_datapoints.append(get_percent_pos(biden_classifications))
        labels.append(str(cur_time.month) + "-" + str(cur_time.day) + "-" + str(cur_time.year) + " " + str(cur_time.hour) + ":00")

        cur_time += dp_delta

    return trump_datapoints, biden_datapoints, labels

def create_var(data, var_name):
    return var_name + " = " + str(data) + ";\n"

def write_js_file(trump, biden, labels, filename):
    js = ""
    js += create_var(trump, "trump_data")
    js += create_var(biden, "biden_data")
    js += create_var(labels, "xlabels")

    with open(filename, 'w') as f:
        f.write(js)

if __name__ == '__main__':
    conn = configure_sqlite('tweets.db')
    cursor = conn.cursor()

    minute_delta = datetime.timedelta(minutes=1)
    hour_delta = datetime.timedelta(hours=1)
    day_delta = datetime.timedelta(days=1)
    week_delta = datetime.timedelta(weeks=1)

    print("Building day.js...")
    trump, biden, labels = get_datapoints(day_delta, hour_delta, conn)
    write_js_file(trump, biden, labels, 'day.js')
    print("day.js complete.")
    
    print("Building week.js...")
    trump, biden, labels = get_datapoints(week_delta, hour_delta, conn)
    write_js_file(trump, biden, labels, 'week.js')
    print("week.js complete.")

