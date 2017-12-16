"""
Export graphs for the Swiss Tweets dataset.

If run as a standalone file, it calls all export_* functions
defined below.
"""
import os
import logging

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.graph_objs as go

from plotter import Plotter


logging.basicConfig(
    format='%(asctime)s - %(name)s:%(levelname)8s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
_logger = logging.getLogger(__name__)


class SwissTweetsPlotter(Plotter):
    """
    Plotter for Swiss Tweets data.
    """

    def __init__(self):
        super().__init__()
        self._setup(self._cfg['swiss']['data_path'],
                    self._cfg['swiss']['output_path'])

    def export_language_plots(self):
        _logger.info('Starting: export language plots')
        lang_map = {
            'en': 'english',
            'fr': 'french',
            'de': 'german',
            'it': 'italian',
            'es': 'spanish',
            'nl': 'dutch',
        }
        # read CSV via pandas
        df = pd.read_csv(
                os.path.join(self.data_dir, 'tweets_by_language.csv'),
                delimiter=',', index_col=None)
        # keep only tweets written in:
        # english, french, german, italian, spanish or dutch
        cond = ((df['language'] == 'en') |
                (df['language'] == 'fr') |
                (df['language'] == 'de') |
                (df['language'] == 'it') |
                (df['language'] == 'es') |
                (df['language'] == 'nl'))
        df = df[cond]
        # apply language mapping to language column
        df['language'] = df['language'].map(lang_map)
        # convert count to numeric
        df['count'] = pd.to_numeric(df['count'])
        # sort by language name
        df.sort_values(by=['language'], inplace=True)
        # form output file path
        ofpath = os.path.join(self.output_dir, 'swiss_lang_bar.html')
        # plot and save
        bar = go.Bar(x=df['language'], y=df['count'],
                     hoverinfo='text',
                     hovertext=["{}: {:,} tweets".format(r.language, r.count) \
                                for r in df.itertuples()],
                     hoverlabel={'bgcolor': 'green'})
        py.plot([bar], filename=ofpath, auto_open=False)
        _logger.info('Finished: export language plots')

    def export_all(self):
        self.export_language_plots()


def main():
    plotter = SwissTweetsPlotter()
    plotter.export_all()


if __name__ == '__main__':
    main()
