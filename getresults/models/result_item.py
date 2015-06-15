from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel

from ..choices import RESULT_ITEM_STATUS

from .result import Result
from .utestid import Utestid


class ResultItem(BaseUuidModel):

    result = models.ForeignKey(Result)

    utestid = models.ForeignKey(Utestid)

    value = models.CharField(
        max_length=25)

    quantifier = models.CharField(
        max_length=3)

    result_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=10,
        choices=RESULT_ITEM_STATUS)

    validation_reference = models.CharField(
        max_length=25,
        null=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.utestid, str(self.result))

    class Meta:
        app_label = 'getresults'
        unique_together = ('result', 'utestid', 'result_datetime')
