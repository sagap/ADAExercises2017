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


class TweetsLeonPlotter(Plotter):
    """
    Plotter for Swiss Tweets data.
    """

    def __init__(self):
        super().__init__()
        self._setup(self._cfg['leon']['data_path'],
                    self._cfg['leon']['output_path'])

    def export_language_plots(self):
        _logger.info('Starting: export language plots')
        # read CSV via pandas
        df = pd.read_csv(os.path.join(self.data_dir, 'tweets_by_language.csv'))
        _logger.info('Finished: export language plots')

    def export_all(self):
        self.export_language_plots()


def main():
    plotter = TweetsLeonPlotter()
    plotter.export_all()


if __name__ == '__main__':
    main()
