# -*- coding: utf-8 -*-

import luigi
from dateutil.relativedelta import relativedelta
from luigi.contrib.s3 import S3FlagTarget
from luigi.contrib.spark import PySparkTask
from taxfix.decorators import aws_credentials
from taxfix.pipeline.historical import LoadHistoricalData

from pyspark.sql.context import SQLContext
from taxfix.dimensions import Dimensions, SUBMISSION_SUCCESS_EVENT, DATE_OCCURRENCE
from taxfix.pipeline.abstract import AbstractLoadToRedshift
from taxfix.utils import s3_path_to_s3n, s3_bucket


class DailyDimension(PySparkTask):
    """
    Creates a dimension table for historical data
    """
    date = luigi.DateParameter()
    model = luigi.Parameter()

    def output(self):
        """
        The output that this Task produces.

        The output of the Task determines if the Task needs to be run--the task
        is considered finished.

        All the monthly weather data will be stored in the source of truth in the
        S3 bucket.

        """
        path = "/dimensions/{model}/{date:%Y%m%d}/".format(model=self.model)
        return S3FlagTarget(path=s3_bucket(relative_path=path.format(date=self.date)))

    @aws_credentials
    def main(self, sc, *args):
        """
        Called by the pyspark_runner with a SparkContext

        :param sc: SparkContext
        :type sc: pyspark.SparkContext
        :param args: arguments list
        """
        sql_context = SQLContext(sparkContext=sc)

        # get last day to process
        last_day = self.date - relativedelta(days=1)
        s3_glob = s3_bucket(relative_path='/events/*.json'.format(date=last_day))
        input_path = s3_path_to_s3n(path=s3_glob)
        output_path = s3_path_to_s3n(path=self.output().path)

        # read from raw data
        raw_df = sql_context.read.json(path=input_path)

        # creates the dimension
        dimension = Dimensions(spark_context=sc)
        df = dimension.generate_dimension(
            raw_df=raw_df,
            date=last_day,
            inserted_at=self.date,
            event=self.model
        )

        # writes it to s3
        df.write.json(path=s3_path_to_s3n(path=output_path))


class DimensionToRedshift(AbstractLoadToRedshift):
    """
    Loads the data from S3 to Redshift
    """
    date = luigi.DateParameter()
    model = luigi.Parameter()

    # configurations
    table = prune_table = 'dimensions.{model}'.format(str(model))
    prune_column = DATE_OCCURRENCE

    columns = (
        ('user_id', 'VARCHAR(50)'),
        ('manufacturer', 'VARCHAR(50)'),
        ('model', 'VARCHAR(50)'),
        (DATE_OCCURRENCE, 'TIMESTAMP'),
        ('inserted_at', 'TIMESTAMP')
    )

    def requires(self):
        """
        The Tasks that this Task depends on.
        """
        return DailyDimension(date=self.date, model=self.model)

    @property
    def prune_date(self):
        """
        Date to prune the table, for daily dimensions, keep maximum of 1 month.
        """
        return self.date - relativedelta(months=1)
