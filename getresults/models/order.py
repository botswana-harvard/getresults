from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from getresults_aliquot.models import Aliquot

from .panel import Panel


class Order(BaseUuidModel):

    order_identifier = models.CharField(
        max_length=50,
        unique=True,
    )

    order_datetime = models.DateTimeField(null=True)

    panel = models.ForeignKey(Panel)

    aliquot = models.ForeignKey(Aliquot)

    specimen_identifier = models.CharField(
        max_length=50,
    )

    action_code = models.CharField(
        max_length=1,
        null=True)

    report_type = models.CharField(
        max_length=1,
        null=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.order_identifier, self.panel)

    class Meta:
        app_label = 'getresults'
        ordering = ('order_identifier', )
