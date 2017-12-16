# -*- coding: utf-8 -*-
import nltk
nltk.data.path=["."]

from textblob import TextBlob
# textblob classes for English
from textblob.en.taggers import NLTKTagger as PatternTaggerEn
from textblob.en.sentiments import PatternAnalyzer as PatternAnalyzerEn
# textblob classes for French
from textblob_fr import PatternTagger as PatternTaggerFr
from textblob_fr import PatternAnalyzer as PatternAnalyzerFr
# textblob classes for German
from textblob_de import PatternTagger as PatternTaggerDe
from textblob_de import PatternAnalyzer as PatternAnalyzerDe

# instantiate objects
objs = {
  "en": {  # english
    "pos_tagger": PatternTaggerEn(),
    "analyzer": PatternAnalyzerEn(),
  },
  "fr": {  # french
    "pos_tagger": PatternTaggerFr(),
    "analyzer": PatternAnalyzerFr(),
  },
  "de": {  # german
    "pos_tagger": PatternTaggerDe(),
    "analyzer": PatternAnalyzerDe(),
  }
}

samples = [
  ("en", u"I am very happy!"),
  ("fr", u"Je suis très heureux!"),
  ("de", u"Ich bin sehr glücklich!"),
]

for lang, text in samples:
  blob = TextBlob(text, **objs[lang])
  # polarity (double):
  #   - (0.0, 1.0] positive
  #   - (0.0) neutral
  #   - [-1.0, 0) negative
  polarity, subjectivity = blob.sentiment  # need to do it this way!
  print(lang, polarity)
