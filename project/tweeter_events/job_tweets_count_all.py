import pyspark

jobName="TC-by-E"
sc = pyspark.SparkContext(appName=jobName)
sqlc = pyspark.sql.SQLContext(sc)

categorisers = {
    # 2013
    'Pope Francis':
        lambda r: 'pope' in r and 'francis' in r,
    'Boston Marathon Bombing':
        lambda r: ('boston' in r or 'marathon' in r) and 'bomb' in r,
    'Birth of Prince George':
        lambda r: 'prince' in r and 'george' in r,
    'Twerking':
        lambda r: '#twerk' in r,
    'Death of Nelson Mandela':
        lambda r: 'nelson' in r or 'mandela' in r,
    # 2014
    'Ferguson shooting':
        lambda r: 'ferguson' in r or 'michaelbrown' in r,
    'Fappening':
        lambda r: 'fappening' in r,
    'iPhone 6 release':
        lambda r: 'iphone6' in r,
    'Ebola':
        lambda r: 'ebola' in r,
    'Rosetta lands on comet':
        lambda r: 'rosetta' in r and 'comet' in r,
    '#BreakTheInternet (Kim)':
        lambda r: 'breaktheinternet' in r,
    'FIFA World Cup':
        lambda r: 'worldcup' in r or 'mundial' in r or 'mondial' in r,
    # 2015
    'Grexit':
        lambda r: 'grexit' in r,
    'ISIS':
        lambda r: 'isis' in r,
    'Refugee Crisis':
        lambda r: '#refugeeswelcome' in r or 'syria' in r \
                    or 'refugeecrisis' in r or 'refugee crisis' in r,
    'Charlie Hebdo attack':
        lambda r: 'jesuischarlie' in r or 'Charlie Hebdo' in r,
    'BlackLivesMatter':
        lambda r: 'blacklivesmatter' in r,
    'Caitlyn Jenner':
        lambda r: 'caitlynjenner' in r,
    'Germanwings plane crash':
        lambda r: 'germanwings' in r,
    # 2016
    'Rio Olympic Games':
        lambda r: 'rio2016' in r,
    'US Elections':
        lambda r: 'election2016' in r or 'clinton' in r or 'trump' in r,
    'PokemonGo':
        lambda r: 'pokemongo' in r or 'pokemon' in r or 'niantic' in r,
    'Brexit':
        lambda r: 'brexit' in r,
    'Game Of Thrones':
        lambda r: '#got' in r or 'gameofthrones' in r \
                    or 'game of thrones' in r or 'winter is coming' in r \
                    or 'jon snow' in r,
}

def categorise(row):
    for cat, func in categorisers.iteritems():
        if func(row):
            return cat, 1

# tweets = sc.textFile("./data/sample.tsv") \
tweets = sc.textFile("hdfs:///datasets/tweets-leon") \
           .filter(lambda row: len(row.split('\t')) == 5) \
           .map(lambda row: row.lower()) \
           .map(lambda row: categorise(row)) \
           .filter(lambda row: row is not None) \
           .reduceByKey(lambda x, y: x+y) \
           .cache()

sqlc.createDataFrame(tweets).write \
    .format('com.databricks.spark.csv') \
    .save('counts.csv')

# ('FIFA World Cup', 11 304 887)
# ('Refugee Crisis', 5 806 856)
# ('Game Of Thrones', 5 024 365)
# ('Grexit', 32 968)
# ('Death of Nelson Mandela', 11 797 018)
# ('Pope Francis', 434 198)
# ('Boston Marathon Bombing', 512 680)
# ('Twerking', 632 032)
# ('ISIS', 26 920 449)
# ('Ebola', 1 726 123)
# ('PokemonGo', 3 910 023)
# ('Fappening', 32 233)
# ('Charlie Hebdo attack', 645 356)
# ('Birth of Prince George', 196 451)
# ('Brexit', 14 995)
# ('Rio Olympic Games', 54 982)
# ('BlackLivesMatter', 245 278)
# ('Ferguson shooting', 3 113 358)
# ('Caitlyn Jenner', 88 408)
# ('#BreakTheInternet (Kim)', 3 583 959)
# ('Germanwings plane crash', 35 288)
# ('iPhone 6 release', 442 248)
# ('US Elections', 7 425 724)
# ('Rosetta lands on comet', 19 125)
