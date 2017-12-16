import pyspark
from dateutil import parser


jobName="tweets-by-day"
sc = pyspark.SparkContext(appName=jobName)
sc.addPyFile("dependencies.zip")
sqlc = pyspark.sql.SQLContext(sc)


def format_date(dt):
    r = parser.parse(dt)
    return '-'.join([str(r.year), str(r.month), str(r.day)])


tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
           .filter(lambda row: len(row.split('\t')) == 5) \
           .map(lambda row: row.split('\t')) \
           .map(lambda row: (format_date(row[2]), 1)) \
           .reduceByKey(lambda x, y: x+y)

sqlc.createDataFrame(tweets).write \
    .format('com.databricks.spark.csv') \
    .save('tweets_by_day.csv')
