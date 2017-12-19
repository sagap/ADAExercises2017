"""
PySpark job to find the tweets per day for each event.

To run this job on the cluster, do the following:
    1. Put this script, event.py and the events file (events_leon.csv)
       in a directory of your choice in the master node.
    2. Do not rename any file.
    3. Run the job:
        PYTHONIOENCODING=utf8 spark-submit \
        --master yarn \
        --num-executors 17 \
        --executor-cores 5 \
        --executor-memory 19G \
        job_leon_daily_tweets.py
"""

import pyspark
import event

jobName = "tweets-by-day-leon"
sc = pyspark.SparkContext(appName=jobName)
sqlc = pyspark.sql.SQLContext(sc)


def format_date(dt):
    tokens = dt.split(' ')
    return '-'.join((tokens[2], tokens[1], tokens[5]))


def account_tweet(row):
    dt, text = row
    wbag = word_bag(text)
    for evt in eparser.event_list:
        if evt.matches(wbag):
            yield (','.join([evt.event_id, dt]), 1)


def word_bag(text):
    text = ''.join([x for x in text if x.isalpha() or x in '1234567890 '])
    word_bag = frozenset(text.split())
    return word_bag


# add Python dependencies
sc.addPyFile('event.py')
# add CSV file containing event definitions
sc.addFile('events_leon.csv')


# load events
events_path = pyspark.SparkFiles.get('events_leon.csv')
eparser = event.EventParser(events_path)


# map-reduce on tweets
tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
    .filter(lambda row: len(row.split('\t')) == 5) \
    .map(lambda row: row.split('\t')) \
    .filter(lambda row: len(row[2].split(' ')) == 6) \
    .map(lambda row: (format_date(row[2]), row[4].lower())) \
    .flatMap(lambda row: account_tweet(row)) \
    .filter(lambda row: row is not None) \
    .reduceByKey(lambda x, y: x + y) \
    .cache()

sqlc.createDataFrame(tweets).coalesce(32).cache() \
    .map(lambda x: ",".join(map(str, x))) \
    .saveAsTextFile("by_day_all_leon.csv")
