#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Total SUBMISSION_SUCCESS events
Total REGISTRATION_INITIATED events

Both can be split into the following dimensions:
- Date
- Platform
"""

import os
from datetime import datetime

from sparktestingbase.sqltestcase import SQLTestCase

from pyspark.sql.context import SQLContext
from taxfix.dimensions import Dimensions, EVENTS_SCHEMA, SUBMISSION_SUCCESS_EVENT, REGISTRATION_INITIATED_EVENT
from tests import ROOT_PATH


class TestDimensions(SQLTestCase):
    def test_submission_success_dimension(self):
        now = datetime(2018, 2, 27)
        sql_context = SQLContext(sparkContext=self.sc)
        raw_df = sql_context.read.json(os.path.join(ROOT_PATH, 'assets/*.json'))
        dimension = Dimensions(spark_context=self.sc)
        df = dimension.generate_dimension(raw_df=raw_df, inserted_at=now, event=SUBMISSION_SUCCESS_EVENT)
        self.assertListEqual(df.columns, [
            "user_id",
            "manufacturer",
            "model",
            "date_occurrence",
            "inserted_at"
        ])

        expected_df = sql_context.createDataFrame(data=[(
            '0A52CDC6-DDDC-4F7D-AA24-4447F6AF2689',
            'Apple',
            'iPhone8,4',
            datetime(2018, 1, 30, 18, 13, 51),
            datetime(2018, 2, 27, 0, 0))
        ], schema=EVENTS_SCHEMA)
        self.assertEqual(df.collect(), expected_df.collect())

    def test_registration_initiated_dimension(self):
        now = datetime(2018, 2, 27)
        sql_context = SQLContext(sparkContext=self.sc)
        raw_df = sql_context.read.json(os.path.join(ROOT_PATH, 'assets/*.json'))
        dimension = Dimensions(spark_context=self.sc)
        df = dimension.generate_dimension(raw_df=raw_df, inserted_at=now, event=REGISTRATION_INITIATED_EVENT)
        self.assertListEqual(df.columns, [
            "user_id",
            "manufacturer",
            "model",
            "date_occurrence",
            "inserted_at"
        ])

        expected_df = sql_context.createDataFrame(data=[(
            '8e0302a3-2184-4592-851d-b93c32e410ab',
            'apple',
            'iphone8,4',
            datetime(2018, 2, 3, 18, 28, 12),
            datetime(2018, 2, 27, 0, 0))
        ], schema=EVENTS_SCHEMA)
        self.assertEqual(df.collect(), expected_df.collect())
