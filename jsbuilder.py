import sqlite3
import datetime
from collections import defaultdict
import datetime # for benchmarking only, not required.

def configure_sqlite(dbname):
    try:
        conn = sqlite3.connect(dbname)
    except:
        print("Unable to open Sqlite database '" + str(dbname) + "', exiting.")

    cursor = conn.cursor()

    # Check if table datapoints already exists
    if not table_exists("datapoints", cursor):
        # If not, create it
        cursor.execute("CREATE TABLE datapoints (candidate text, time text, percentage text)")
        conn.commit()

    return conn

def table_exists(tablename, cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + tablename + "'")
    result = cursor.fetchall()

    return len(result) > 0

def get_max_time(table, conn):
    return get_bound_time(table, "MAX", conn)

def get_min_time(table, conn):
    return get_bound_time(table, "MIN", conn)

def get_bound_time(table, func, conn):
    cursor = conn.cursor()
    max_time = cursor.execute("SELECT " + str(func) + "(datetime(time)) FROM " + str(table))
    max_time = max_time.fetchone()[0]
   
    if max_time:
        max_time = datetime.datetime.strptime(max_time, "%Y-%m-%d %H:%M:%S")
    else:
        print("WARNING: returned NULL " + str(func) + " time for table '" + str(table) + "'")

    return max_time

def get_percent_by_label(classifications):
    percentages = defaultdict(lambda: 0)

    for c in classifications:
        percentages[c] += 1

    for label, value in percentages.items():
        percentages[label] = float(value) / float(len(classifications))

    return percentages

def get_percent_pos(classifications):
    p = get_percent_by_label(classifications)
    
    return p['pos'] * 100

def get_datapoints(window_delta, conn):
    trump_datapoints = []
    biden_datapoints = []
    labels = []

    cursor = conn.cursor()
    end_time = get_max_time("datapoints", conn)
    start_time = end_time - window_delta
    datapoints = cursor.execute("SELECT candidate, datetime(time), percentage time FROM datapoints WHERE time BETWEEN '" + start_time.isoformat() + "' AND '" + end_time.isoformat() + "'")
    datapoints = datapoints.fetchall()

    for datapoint in datapoints:
        candidate, time, percentage = datapoint
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

        if candidate == "Donald Trump":
            trump_datapoints.append(percentage)
        elif candidate == "Joe Biden":
            biden_datapoints.append(percentage)

        label = str(time.month) + "-" + str(time.day) + "-" + str(time.year) + " " + str(time.hour) + ":00"

        # Ugly hack. There's two datapoints to every label, and we only want to generate one label for both.
        if len(labels) <= 0 or labels[-1] != label:
            labels.append(label)

    trump_datapoints = [float(x) for x in trump_datapoints]
    biden_datapoints = [float(x) for x in biden_datapoints]

    return trump_datapoints, biden_datapoints, labels

def calculate_datapoints(conn):
    cursor = conn.cursor()
    # Calculate average percentage positive over hourly intervals
    dp_delta = datetime.timedelta(hours=1)

    print("Getting last calculated datapoint time...")
    # Begin calculating data after the last cached datapoint
    start_time = get_max_time("datapoints", conn)

    # If there aren't any datapoints already in the database, we'll calculate starting at the beginning of the raw data
    if not start_time:
        print("Getting first raw datapoint time...")
        start_time = get_min_time("tweets", conn)

    # Round the start time to the beginning of the hour, so we do hour intervals that line up with normal time
    start_time = start_time.replace(second=0, microsecond=0, minute=0)

    print("Getting last raw datapoint time...")
    # Finish calculating data with the final raw datapoint
    max_time = get_max_time("tweets", conn)

    cur_time = start_time
    trump_datapoints = []
    biden_datapoints = []
    labels = []
    trump_tags = ['@realDonaldTrump', '@POTUS']
    biden_tags = ['@JoeBiden']

    print("Start time: " + str(start_time))
    print("End time: " + str(max_time))

    print("Beginning hourly interval average calculations...")
    # Go through new data hour by hour, but don't do the final (likely current) incomplete hour
    while cur_time + dp_delta < max_time:
        print("Current calculation hour is " + str(cur_time))
        trump_classifications = []
        biden_classifications = []
        interval_start = cur_time
        interval_end = cur_time + dp_delta

        # Grab all the tweets in our hour interval
        rows = cursor.execute("SELECT tag, classification, datetime(time) time FROM tweets WHERE time BETWEEN '" + interval_start.isoformat() + "' AND '" + interval_end.isoformat() + "'")
        results = rows.fetchall()

        # Sort results into trump or biden and grab the actual neg/pos classification
        for result in results:
            if result[0] in trump_tags:
                trump_classifications.append(result[1])
            if result[0] in biden_tags:
                biden_classifications.append(result[1])

        # Get the percentage of the tweets that were classified positive
        trump_percent = get_percent_pos(trump_classifications)
        biden_percent = get_percent_pos(biden_classifications)

        print("Trump %: " + str(trump_percent))
        print("Biden %: " + str(biden_percent))

        # Put the calculated datapoint for each candidate into the datapoints table
        cursor.execute("INSERT INTO datapoints VALUES(?,?,?)", ("Donald Trump", cur_time.isoformat(), trump_percent))
        cursor.execute("INSERT INTO datapoints VALUES(?,?,?)", ("Joe Biden", cur_time.isoformat(), biden_percent))
        conn.commit()

        cur_time += dp_delta

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
    then = datetime.datetime.now()
    conn = configure_sqlite('tweets.db')

    calculate_datapoints(conn)

    day_delta = datetime.timedelta(days=1)
    week_delta = datetime.timedelta(weeks=1)

    print("Building day.js...")
    trump, biden, labels = get_datapoints(day_delta, conn)
    write_js_file(trump, biden, labels, 'day.js')
    print("day.js complete.")
    
    print("Building week.js...")
    trump, biden, labels = get_datapoints(week_delta, conn)
    write_js_file(trump, biden, labels, 'week.js')
    print("week.js complete.")

    now = datetime.datetime.now()
    duration = now - then

    print("JavaScript generation completed in " + str(duration.seconds) + " seconds.")

