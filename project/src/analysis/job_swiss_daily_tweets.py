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
        job_swiss_daily_tweets.py
"""

import pyspark
import event

jobName = "tweets-by-day-leon"
sc = pyspark.SparkContext(appName=jobName)
sqlc = pyspark.sql.SQLContext(sc)


def format_date(dt):
    # dt is in the following format: 2016-01-01T00:30:04Z
    # we keep only 2016-01-01
    tokens = dt.split('T')
    return str(tokens[0])


def account_tweet(row):
    dt, text = row
    wbag = word_bag(text)
    for evt in eparser.event_list:
        if evt.matches(wbag):
            yield (';'.join([evt.event_id, dt]), 1)


def word_bag(text):
    text = ''.join([x for x in text if x.isalpha() or x in '1234567890 '])
    word_bag = frozenset(text.split())
    return word_bag


# add Python dependencies
sc.addPyFile('event.py')
# add CSV file containing event definitions
sc.addFile('events_swiss.csv')


# load events
events_path = pyspark.SparkFiles.get('events_swiss.csv')
eparser = event.EventParser(events_path)


# map-reduce on tweets
tweets = sqlc.jsonFile('hdfs:///datasets/swiss-tweet/*.json') \
    .map(lambda row: (format_date(row['_source']['published']),
                      row['_source']['main'].lower())) \
    .flatMap(lambda row: account_tweet(row)) \
    .filter(lambda row: row is not None) \
    .reduceByKey(lambda x, y: x + y) \
    .cache()

sqlc.createDataFrame(tweets).coalesce(32).cache() \
    .map(lambda x: ",".join(map(str, x))) \
    .saveAsTextFile("by_day_all_swiss.csv")
