import pyspark

jobName="Tweets count"
sc = pyspark.SparkContext(appName=jobName)
sqlc = pyspark.sql.SQLContext(sc)

# open file
tweets = sc.textFile("hdfs:///datasets/tweets-leon")
# split row into columns
tweets = tweets.map(lambda row: row.split("\t"))
# create spark dataframe
df = sqlc.createDataFrame(
    tweets,
    schema=['language', 'id', 'timestamp', 'username', 'text'])

# group by language and count
groups = df.groupby('language').count()
# write output file
groups.coalesce(1).write \
    .format('com.databricks.spark.csv') \
    .option("header", "true") \
    .save('/buffer/dona/lang_counts.csv.dona')

# Run this job with the following command on the cluster:
# spark-submit \
#   --master yarn \
#   --packages com.databricks:spark-csv_2.10:1.5.0 \
#   --num-executors 128 --executor-cores 16 \
#   tweeter_events-dona/job_tweets_by_lang.py
