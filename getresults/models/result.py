from django.db import models

from simple_history.models import HistoricalRecords

from .export_mixin import ExportMixin
from .panel import Panel
from .order import Order
from .validation_mixin import ValidationMixin


class Result(ExportMixin, ValidationMixin, models.Model):

    result_identifier = models.CharField(
        max_length=25,
        null=True)

    order = models.ForeignKey(Order)

    specimen_identifier = models.CharField(
        max_length=25,
        null=True)

    collection_datetime = models.DateTimeField(null=True)

    status = models.CharField(
        max_length=1,
        null=True)

    analyzer_name = models.CharField(
        max_length=25,
        null=True)

    analyzer_sn = models.CharField(
        max_length=25,
        null=True)

    operator = models.CharField(
        max_length=25,
        null=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.result_identifier, str(self.order))

    class _Meta:
        app_label = 'getresults'
        unique_together = ('result_identifier', 'collection_datetime')
