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
        # plot and save
        # form output file path for bar chart
        ofpath = os.path.join(self.output_dir, 'swiss_lang_bar.html')
        layout = go.Layout(title='Tweet counts by language (Swiss Tweets)')
        bar = go.Bar(x=df['language'], y=df['count'],
                     hoverinfo='text',
                     hovertext=["{}<br>{:,} tweets".format(r.language, r.count)
                                for r in df.itertuples()],
                     hoverlabel={'bgcolor': 'green'})
        fig = go.Figure(data=[bar], layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        # form output file path for pie chart
        ofpath = os.path.join(self.output_dir, 'swiss_lang_pie.html')
        pie = go.Pie(labels=df['language'], values=df['count'], sort=False)
        py.plot([pie], filename=ofpath, auto_open=False)
        _logger.info('Finished: export language plots')

    def export_daily_count_plots(self):
        _logger.info('Starting: export daily count plots')
        # read CSV via pandas
        df = pd.read_csv(
            os.path.join(self.data_dir, 'tweets_by_day.csv'),
            delimiter=',', index_col=None)
        # convert count to numeric
        df['count'] = pd.to_numeric(df['count'])
        df['date'] = pd.to_datetime(df['date'])
        # sort by date
        df.sort_values(by=['date'], inplace=True)
        # form output file path for scatter plot
        ofpath = os.path.join(self.output_dir, 'swiss_daily.html')
        layout = go.Layout(title='Tweet counts by day (Swiss Tweets)')
        scatter = go.Scatter(x=df['date'], y=df['count'],
                             hoverinfo='text+x',
                             hovertext=["{:,} tweets".format(r.count)
                                        for r in df.itertuples()])
        fig = go.Figure(data=[scatter], layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        _logger.info('Finished: export daily count plots')

    def export_counts_sentimental(self, *args):
        _logger.info('Starting: export sentiment count plot')
        # read results into a dataframe
        results = pd.read_csv(
            os.path.join(self.data_dir, 'results', 'sentimental_counts.csv'),
            delimiter=',', index_col=None)
        # make necessary convertions
        results['event_id'] = pd.to_numeric(results['event_id'])
        results['count'] = pd.to_numeric(results['count'])
        results['polarity'] = results['polarity'].astype(str)
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
        results = results.mask(results['polarity'].str.contains('UNKNOWN')) \
                         .dropna()
        results.sort_values(by='polarity', inplace=True)

        # replace count with percentage in results
        def gb(group):
            gsum = group['count'].sum()
            group['count'] = group['count'] \
                .apply(lambda x: round(x / gsum * 100.0, 2))
            results.loc[group.index.values[0]] = group
        results.groupby(level=0).apply(gb)
        # start building plot...
        traces = [
            go.Bar(x=df['polarity'], y=df['count'],
                   name=df['event_name'].iloc[0],
                   hoverinfo='text+name',
                   hovertext=["{:,}%".format(r.count)
                              for r in df.itertuples()])
            for df in self._slice_by_event_ids(results, *args)
        ]
        # form output file path for scatter plot
        ofpath = os.path.join(self.output_dir, 'sentiment_swiss_all.html')
        layout = go.Layout(title='Cummulative polarity plot '
                                 '(click on the legend items to toggle them)',
                           barmode='group',
                           xaxis=dict(title='Polarity'),
                           yaxis=dict(title='Percentage (%)'))
        fig = go.Figure(data=traces, layout=layout)
        py.plot(fig, filename=ofpath, auto_open=False)
        _logger.info('Finished: export sentiment count plot')

    def export_all(self):
        self.export_language_plots()
        self.export_daily_count_plots()
        self.export_counts_multi_plot()
        self.export_counts_sentimental()


def main():
    plotter = SwissTweetsPlotter()
    plotter.export_all()


if __name__ == '__main__':
    main()
