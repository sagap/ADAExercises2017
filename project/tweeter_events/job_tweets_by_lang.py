import pyspark

jobName="Tweets count"
sc = pyspark.SparkContext(appName=jobName)
sqlc = pyspark.sql.SQLContext(sc)

# open file
tweets = sc.textFile("hdfs:///datasets/tweets-leon")
# split row into columns
tweets = tweets \
            .filter(lambda row: len(row.split("\t")) == 5) \
            .map(lambda row: row.split("\t"))
# create spark dataframe
df = sqlc.createDataFrame(
    tweets,
    schema=['language', 'id', 'timestamp', 'username', 'text'])

# group by language and count
groups = df.groupby('language').count()
# write output file
groups.coalesce(1).write \
    .format('com.databricks.spark.csv') \
    .options(header='true') \
    .save('lang_counts.csv')

# Run this job with the following command on the cluster:
# spark-submit \
#   --master yarn \
#   --packages com.databricks:spark-csv_2.10:1.5.0 \
#   --num-executors 128 --executor-cores 16 \
#   tweeter_events-dona/job_tweets_by_lang.py
#
# Results are:
# +----------+-------------+
# | language |       count |
# +----------+-------------+
# | french   |   676529769 |
# | dutch    |   452780443 |
# | italian  |   466666820 |
# | german   |   452126737 |
# | english  | 12488903036 |
# | spanish  |  3439067021 |
# +----------+-------------+
