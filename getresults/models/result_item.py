from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from ..choices import RESULT_ITEM_STATUS

from .result import Result
from .utestid import Utestid


class ResultItem(BaseUuidModel):

    result = models.ForeignKey(Result)

    utestid = models.ForeignKey(Utestid)

    value = models.CharField(
        max_length=25,
        null=True)

    raw_value = models.CharField(
        max_length=25,
        null=True)

    quantifier = models.CharField(
        max_length=3,
        null=True)

    result_datetime = models.DateTimeField(
        null=True)

    status = models.CharField(
        max_length=10,
        choices=RESULT_ITEM_STATUS,
        null=True)

    validation_reference = models.CharField(
        max_length=25,
        null=True)

    sender = models.CharField(
        max_length=25,
        null=True,
        help_text='analyzer or instrument')

    source = models.CharField(
        max_length=25,
        null=True,
        help_text='For example, \'filename\' for CSV or \'ASTM\'')

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.utestid, str(self.result))

    class Meta:
        app_label = 'getresults'
        unique_together = ('result', 'utestid', 'result_datetime')
