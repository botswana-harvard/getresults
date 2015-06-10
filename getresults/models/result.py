from django.db import models

from simple_history.models import HistoricalRecords

from .panel import Panel
# from .import_history import ImportHistory
# from .export_history import ExportHistory


class Result(models.Model):

    result_identifier = models.CharField(
        max_length=25)

    collection_datetime = models.DateTimeField()

    panel = models.ForeignKey(Panel)

    analyzer_name = models.CharField(
        max_length=25)

    analyzer_sn = models.CharField(
        max_length=25)

    operator = models.CharField(
        max_length=25)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.result_identifier, str(self.panel))

    class _Meta:
        app_label = 'getresults'
        unique_together = ('result_identifier', 'collection_datetime')
