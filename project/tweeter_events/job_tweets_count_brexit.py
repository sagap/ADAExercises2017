from pyspark import SparkContext

jobName="Tweets count"
sc = SparkContext(appName=jobName)

tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
           .filter(lambda row: len(row.split('\t')) == 5) \
           .filter(lambda row: "#brexit" in row)
count = tweets.count()
print("***** #brexit:", count)  # should return 1472
