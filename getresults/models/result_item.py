from django.db import models

from simple_history.models import HistoricalRecords

from .result import Result
from .utestid import Utestid
from .validation_mixin import ValidationMixin


class ResultItem(ValidationMixin, models.Model):

    result = models.ForeignKey(Result)

    utestid = models.ForeignKey(Utestid)

    value = models.CharField(
        max_length=25)

    quantifier = models.CharField(
        max_length=3)

    result_datetime = models.DateTimeField()

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.utestid, str(self.result))

    class Meta:
        app_label = 'getresults'
        unique_together = ('result', 'utestid', 'result_datetime')
