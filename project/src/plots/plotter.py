"""
Plotter for tweet data.
"""
import os
import logging
import abc

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

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def output_dir(self):
        return self._output_dir

