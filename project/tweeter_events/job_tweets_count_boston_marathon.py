from pyspark import SparkContext

jobName="Tweets count"
sc = SparkContext(appName=jobName)

tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
           .filter(lambda row: len(row.split('\t')) == 5) \
           .filter(lambda row: "boston" in row.lower() and \
           					   "marathon" in row.lower() and \
           					   "bomb" in row.lower())
count = tweets.count()
print("***** Boston marathon bombing:", count)  # should return 154268
