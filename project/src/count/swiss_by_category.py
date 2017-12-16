import os
import pandas as pd
import json

from dateutil import parser

DATA_DIR = 'swiss-tweet'

def json_files():
    """Generator yielding the JSON data files for swiss-tweet."""
    for (i, file_) in enumerate(os.listdir(DATA_DIR)):
        if file_.endswith('.json'):
            yield os.path.join(DATA_DIR, file_)

def count_all_tweets():
    return sum((len(pd.read_json(file_)) for file_ in json_files()))

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
        lambda r: 'germanwings' in r and 'crash' in r,
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

counts = {
    k: 0 for k in categorisers.keys()
}


def categorise(row):
    for cat, func in categorisers.items():
        if func(row):
            counts[cat] += 1
            return

def count_by_category():
    for file_ in json_files():
        f = open(file_)
        for o in json.load(f):
            text = o['_source']['main']
            categorise(text)


count_all_tweets()  # 10 828 070
counts_by_category = count_by_category()
