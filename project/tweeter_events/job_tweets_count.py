from pyspark import SparkContext

jobName="Tweets count"
sc = SparkContext(appName=jobName)

tweets = sc.textFile("hdfs:///datasets/tweets-leon")
count = tweets.count()
print("Counted tweets:", count)
