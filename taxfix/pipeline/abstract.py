# -*- coding: utf-8 -*-

import luigi
from luigi.contrib.redshift import S3CopyToTable


class AbstractLoadToRedshift(S3CopyToTable):
    """
    Generict Task for inserting a data set into Redshift from s3.
    """
    aws_access_key_id = luigi.configuration.get_config().get('aws', 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = luigi.configuration.get_config().get('aws', 'AWS_SECRET_ACCESS_KEY', None)
    host = luigi.configuration.get_config().get('redshift', 'host', None)
    database = luigi.configuration.get_config().get('redshift', 'database', None)
    user = luigi.configuration.get_config().get('redshift', 'user', None)
    password = luigi.configuration.get_config().get('redshift', 'password', None)
    copy_options = "format as json 'auto'"

    def s3_load_path(self):
        """
        S3 Load path.
        """
        return self.input().path
