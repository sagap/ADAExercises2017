from pyspark import SparkContext

jobName="Tweets count"
sc = SparkContext(appName=jobName)

tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
           .filter(lambda row: len(row.split('\t')) == 5) \
           .filter(lambda row: "#grexit" in row)
count = tweets.count()
print("***** #grexit:", count)  # should return 3994
