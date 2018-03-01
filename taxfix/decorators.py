# -*- coding: utf-8 -*-
import os
from shutil import rmtree

from pyspark.sql.context import SQLContext


def _remove_metadata_db():
    """
    force remove all spark-warehouse
    """
    derby_path = os.path.join(os.getcwd(), 'spark-warehouse')
    if os.path.exists(derby_path):
        rmtree(derby_path, ignore_errors=True)


def aws_credentials(func):
    """
    Insert the aws credentials to main call function

    """

    def credentials(*args):
        """
        Update the credentials for AWS
        :type sc: pyspark.context.SparkContext
        """
        klass = args[0]
        sc = args[1]
        sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", os.getenv('AWS_ACCESS_KEY_ID'))
        sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", os.getenv('AWS_SECRET_ACCESS_KEY'))
        klass.sql_ctx = SQLContext(sparkContext=sc)
        try:
            return func(*args)
        finally:
            _remove_metadata_db()

    return credentials
