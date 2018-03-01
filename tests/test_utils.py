#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Capture historical forecast for meteorological stations (5 at least)
listed on https://data.gov.uk/dataset/historic-monthly-meteorological-station-data
"""
import unittest

from taxfix.utils import timestamp_to_str


class TestUtils(unittest.TestCase):
    def test_timestamp_to_utc(self):
        self.assertEqual(timestamp_to_str(1406106000), '2014-07-23 09:00:00')
