# -*- coding: utf-8 -*-


import os
from datetime import datetime

import luigi


def timestamp_to_str(epoch):
    """
    Convert a epoch to a string format to be inserted on Redshift

    :type epoch: int
    :param epoch: epoch time
    :rtype: str
    :return: formated date
    """
    date_obj = datetime.utcfromtimestamp(epoch)
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def s3_bucket(relative_path):
    """
    Return a full path of current s3 bucket to materialize steps and final result

    :type relative_path: str
    :param relative_path: relative path to create file
    :return: full path to s3 bucket file
    """
    bucket = luigi.configuration.get_config().get('aws', 'bucket', None)
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    return os.path.join('s3://', bucket, relative_path)


def s3_path_to_s3n(path):
    """
    Return a full path of current s3 bucket to s3n path

    :type path: str
    :param path: relative path to create file
    :return: full path to s3n bucket file
    """

    return path.replace('s3://', 's3n://')
