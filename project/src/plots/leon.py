"""
Export graphs for the Swiss Tweets dataset.

If run as a standalone file, it calls all export_* functions
defined below.
"""
import os
import logging

import pandas as pd

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
        df = pd.read_csv(
            os.path.join(self.data_dir, 'tweets_by_language.csv'),
            delimiter=',', index_col=None)
        # convert count to numeric
        df['count'] = pd.to_numeric(df['count'])
        # sort by language name
        df.sort_values(by=['language'], inplace=True)
        # plot and save
        # form output file path for bar chart
        ofpath = os.path.join(self.output_dir, 'leon_lang_bar.html')
        layout = go.Layout(title='Tweet counts by language (Tweets Leon)')
        bar = go.Bar(x=df['language'], y=df['count'],
                     hoverinfo='text',
                     hovertext=["{}: {:,} tweets".format(r.language, r.count)
                                for r in df.itertuples()],
                     hoverlabel={'bgcolor': 'green'})
        fig = go.Figure(data=[bar], layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        # form output file path for pie chart
        ofpath = os.path.join(self.output_dir, 'leon_lang_pie.html')
        pie = go.Pie(labels=df['language'], values=df['count'], sort=False)
        py.plot([pie], filename=ofpath, auto_open=False)
        _logger.info('Finished: export language plots')

    def export_monthly_count_plots(self):
        _logger.info('Starting: export monthly count plots')
        # read CSV via pandas
        df = pd.read_csv(
            os.path.join(self.data_dir, 'tweets_by_month.csv'),
            delimiter=',', index_col=None)
        # convert count to numeric
        df['count'] = pd.to_numeric(df['count'])
        df['month'] = pd.to_datetime(df['month'])
        # sort by date
        df.sort_values(by=['month'], inplace=True)
        # form output file path for scatter plot
        ofpath = os.path.join(self.output_dir, 'leon_monthly.html')
        layout = go.Layout(title='Tweet counts by month (Tweets Leon)')
        scatter = go.Scatter(x=df['month'], y=df['count'],
                             hoverinfo='text+x',
                             hovertext=["{:,} tweets".format(r.count)
                                        for r in df.itertuples()])
        fig = go.Figure(data=[scatter], layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        _logger.info('Finished: export daily count plots')

    def export_all(self):
        self.export_language_plots()
        self.export_monthly_count_plots()


def main():
    plotter = TweetsLeonPlotter()
    plotter.export_all()


if __name__ == '__main__':
    main()
