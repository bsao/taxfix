# -*- coding: utf-8 -*-
import logging
import os
import sys

import luigi

__author__ = "Robson Luis Monteiro Junior"
__email__ = 'bsao@icloud.com'
__version__ = '0.9.0'

# environment status
ENV = os.environ.get('ENV', 'DEV')

# logger for console
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER = logging.getLogger('taxfix')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)

# paths for monthly data
METEOROLOGICAL_STATION_DATA = 'https://data.gov.uk/dataset/historic-monthly-meteorological-station-data'
STATION_DATA = 'http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/'


def set_aws_env():
    aws_access_key_id = luigi.configuration.get_config().get('aws', 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = luigi.configuration.get_config().get('aws', 'AWS_SECRET_ACCESS_KEY', None)
    if not aws_access_key_id:
        raise ValueError('AWS_ACCESS_KEY_ID should be defined in luigi.cfg')
    if not aws_secret_access_key:
        raise ValueError('AWS_SECRET_ACCESS_KEY should be defined in luigi.cfg')
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key


LOGGER.info('Starting app.')
if ENV in ['DEV', 'LIVE']:
    LOGGER.info('Setting AWS credentials.')
    set_aws_env()
