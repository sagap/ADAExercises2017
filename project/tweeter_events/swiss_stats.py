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

def counts_by_lang():
    """Return the tweet counts by language."""
    langs = {}
    for file_ in json_files():
        f = open(file_)
        for o in json.load(f):
            lang = o['_source']['lang']
            langs[lang] = (langs[lang] + 1) if lang in langs else 1
    return langs

def date_range():
    """Return time period that the tweets span."""
    min_date = None
    max_date = None
    for file_ in json_files():
        f = open(file_)
        dates = [parser.parse(o['_source']['published']) for o in json.load(f)]
        max_date = max(max_date, max(dates)) if max_date is not None else max(dates)
        min_date = min(min_date, min(dates)) if min_date is not None else min(dates)
    return min_date, max_date

def counts_by_region():
    """Return the counts of the tweets per region.

    These regions can be in all possible languages and spelling combinations
    (depends on the user). E.g. Geneva can be written as "Geneve", "Geneva",
    "geneva", "Genève", etc.
    """
    counts = {'NA': 0}
    for file_ in json_files():
        f = open(file_)
        for o in json.load(f):
            if 'source_location' not in o['_source']:
                counts['NA'] += 1
                continue
            loc = o['_source']['source_location']
            counts[loc] = (counts[loc] + 1) if loc in counts else 1
    return counts

def counts_by_sentiment():
    """Return the counts of the tweets per sentiment.

    Possible values for sentiments:
        - NA (missing)
        - NEGATIVE
        - NEUTRAL
        - POSITIVE
    """
    counts = {'NA': 0}
    for file_ in json_files():
        f = open(file_)
        for o in json.load(f):
            if 'sentiment' not in o['_source']:
                counts['NA'] += 1
                continue
            sent = o['_source']['sentiment']
            counts[sent] = (counts[sent] + 1) if sent in counts else 1
    return counts


by_langs = counts_by_lang()
min_date, max_date = date_range()
by_region = counts_by_region()
by_sentiment = counts_by_sentiment()
