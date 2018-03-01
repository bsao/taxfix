from dateutil import parser

from pyspark.sql.functions import lit, UserDefinedFunction
from pyspark.sql.types import StructType, StructField, TimestampType, StringType
from taxfix import LOGGER

SUBMISSION_SUCCESS_EVENT = 'submission_success'
REGISTRATION_INITIATED_EVENT = 'registration_initiated'
TEMP_TABLE = 'events'
DATE_OCCURRENCE = 'date_occurrence'

QUERY = """
SELECT
    anonymous_id as user_id, 
    context_device_manufacturer as manufacturer, 
    context_device_model as model, 
    sent_at as date_occurrence
FROM
    events
"""

EVENTS_SCHEMA = StructType([
    StructField('user_id', StringType(), True),
    StructField('manufacturer', StringType(), True),
    StructField('model', StringType(), True),
    StructField(DATE_OCCURRENCE, TimestampType(), True),
    StructField('inserted_at', TimestampType(), True)
])


class Dimensions(object):
    """
    Total SUBMISSION_SUCCESS events
    Total REGISTRATION_INITIATED events

    Both can be split into the following dimensions:
    - Date
    - Platform
    """

    def __init__(self, spark_context):
        """

        Create the dimension files

        :type spark_context: pyspark.context.SparkContext
        """
        self.spark_context = spark_context
        LOGGER.info('Running context: {}'.format(spark_context.appName))

    def generate_dimension(self, raw_df, inserted_at, event):
        """
        Create a dimension for submission success data

        :param raw_df: Generated dataframe from raw data
        :type raw_df: pyspark.sql.dataframe.DataFrame
        :param inserted_at: date from creation
        :type inserted_at: datetime.datetime
        :param event: which event to create the dimension
        :type event: str
        :rtype: pyspark.sql.dataframe.DataFrame
        :return: a new dataframe with the values
        """

        def _epoch_date(date_str):
            return parser.parse(date_str)

        udf_epoch_date = UserDefinedFunction(_epoch_date, TimestampType())
        df = raw_df.where(raw_df.event == event).cache()
        df.registerTempTable(TEMP_TABLE)
        df = df.sql_ctx.sql(QUERY)
        df = df.withColumn(DATE_OCCURRENCE, udf_epoch_date(df[DATE_OCCURRENCE]))
        df = df.withColumn("inserted_at", lit(inserted_at))
        df = df.select(*EVENTS_SCHEMA.names)
        LOGGER.info('Calculating submission success')
        return df
