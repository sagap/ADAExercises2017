from pyspark import SparkContext

jobName="Tweets count"
sc = SparkContext(appName=jobName)

tweets = sc.textFile("hdfs:///datasets/tweets-leon")
count = tweets.count()
print("Counted tweets:", count)  # should return 17 984 217 710
