"""
Export graphs for the Tweets Leon dataset.

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

DATA_DIR = '../data/leon'
OUTPUT_DIR = 'plots.out/leon'


logging.basicConfig(
    format='%(asctime)s - %(name)s:%(levelname)8s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
_logger = logging.getLogger(__name__)


class TweetsLeonPlotter(object):
    """
    Plotter for Tweets Leon data.
    """

    def __init__(self):
        self._setup()

    def export_language_plots(self):
        _logger.info('Starting: export language plots')
        # read CSV via pandas
        df = pd.read_csv(os.path.join(self.data_dir, 'tweets_by_language.csv'))

        _logger.info('Finished: export language plots')

    def export_all(self):
        self.export_language_plots()

    def _setup(self):
        # get this file's path
        this_dir, _ = os.path.split(os.path.abspath(__file__))
        # setup output directory
        self._output_dir = os.path.join(this_dir, OUTPUT_DIR)
        if not os.path.exists(self.output_dir):
            _logger.info('Creating output directory: %s', self.output_dir)
            os.makedirs(self.output_dir)
        else:
            _logger.warning('Output directory exists, files will be overwritten!')
        # check for data directory
        self._data_dir = os.path.join(this_dir, DATA_DIR)
        if not os.path.exists(self.data_dir):
            _logger.error('Could not find data directory! Expected in:\n'
                          '\t%s', self.data_dir)

    @property
    def output_dir(self):
        return self._output_dir

    @property
    def data_dir(self):
        return self._data_dir


def main():
    plotter = TweetsLeonPlotter()
    plotter.export_all()


if __name__ == '__main__':
    main()
