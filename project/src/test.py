import platform
from pyspark import SparkContext

jobName="My Name"
sc = SparkContext(appName=jobName)
print(platform.platform())
