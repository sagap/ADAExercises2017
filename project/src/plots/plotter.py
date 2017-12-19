"""
Plotter for tweet data.
"""
import os
import logging
import abc

import pandas as pd
import numpy as np

import plotly.offline as py
import plotly.graph_objs as go

import configparser

logging.basicConfig(
    format='%(asctime)s - %(name)s:%(levelname)8s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
_logger = logging.getLogger(__name__)


class Plotter(abc.ABC):
    """
    Plotter (abstract) class for generating various plots out of the data.
    """

    def __init__(self):
        self._cfg = self._read_config()

    @staticmethod
    def _read_config():
        """Read the configuration file and return the configuration object."""
        if not os.path.exists('plots.cfg'):
            _logger.error('Configuration file lookup failed: ("plots.cfg")')
            _logger.error('Make sure the configuration file exists!')
            raise OSError('Configuration file not found!')
        config = configparser.ConfigParser()
        config.read('plots.cfg')
        return config

    def _setup(self, data_dir, output_dir):
        """Setup the data and output directories."""
        # get this script's path, in case it is needed
        this_dir, _ = os.path.split(os.path.abspath(__file__))
        # setup output directory
        self._output_dir = os.path.join(this_dir, output_dir) \
            if not os.path.isabs(output_dir) else output_dir
        if not os.path.exists(self.output_dir):
            _logger.info('Creating output directory: %s', self.output_dir)
            os.makedirs(self.output_dir)
        else:
            _logger \
                .warning('Output directory exists, files will be overwritten!')
        # check for data directory
        self._data_dir = os.path.join(this_dir, data_dir) \
            if not os.path.isabs(data_dir) else data_dir
        if not os.path.exists(self.data_dir):
            _logger.error('Could not find data directory! Expected in: '
                          '%s', self.data_dir)

    def export_counts_multi_plot(self, *args):
        """Export multiple time series into a single plot.

        Arguments:
            - args: the IDs of the events to plot. if None, exports all events.
        """
        _logger.info('Starting: export daily count multiplot')
        # read results into a dataframe
        results = pd.read_csv(
            os.path.join(self.data_dir, 'results', 'daily_counts.csv'),
            delimiter=',', index_col=None)
        # make necessary convertions
        results['event_id'] = pd.to_numeric(results['event_id'])
        results['date'] = pd.to_datetime(results['date'])
        results['count'] = pd.to_numeric(results['count'])
        results.set_index('event_id', inplace=True)  # set index
        # read events into a dataframe
        events = pd.read_csv(
            os.path.join(self.data_dir, 'events', 'events.csv'),
            delimiter=';', index_col=None)
        # make necessary convertions
        events['id'] = pd.to_numeric(events['id'])
        events['date'] = pd.to_datetime(events['date'])
        events.set_index('id', inplace=True)  # set index
        # assign names in results from events dataframe
        results['event_name'] = events['name']
        # sort by date
        results.sort_values(by='date', inplace=True)
        # start building plot...
        traces = [
            go.Scatter(x=df['date'], y=df['count'],
                       name=df['event_name'].iloc[0],
                       hoverinfo='y+name', line=dict(width='1.5'))
            for df in self._slice_by_event_ids(results, *args)
        ]
        # form output file path for scatter plot
        ofpath = os.path.join(self.output_dir, 'counts_all.html')
        layout = go.Layout(title='Cummulative analysis plot '
                                 '(click on the legend items to toggle them)',
                           xaxis=dict(title='Day'),
                           yaxis=dict(title='Number of tweets'))
        fig = go.Figure(data=traces, layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        _logger.info('Finished: export daily count multiplot')

    @staticmethod
    def _slice_by_event_ids(results, *args):
        if not args:
            args = np.unique(results.index.values)
        for i in args:
            yield results.loc[i]

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def output_dir(self):
        return self._output_dir
