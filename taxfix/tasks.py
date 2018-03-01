# -*- coding: utf-8 -*-

from datetime import datetime

import luigi

from taxfix.dimensions import SUBMISSION_SUCCESS_EVENT, REGISTRATION_INITIATED_EVENT
from taxfix.pipeline.dimensions import DimensionToRedshift


class DimensionLoader(luigi.WrapperTask):
    """
    Create or update the dimensions tables
    """
    now = datetime.now()

    def requires(self):
        """
        Execute all subtasks for this task
        """
        return [
            DimensionToRedshift(date=self.now, model=SUBMISSION_SUCCESS_EVENT),
            DimensionToRedshift(date=self.now, model=REGISTRATION_INITIATED_EVENT)
        ]
