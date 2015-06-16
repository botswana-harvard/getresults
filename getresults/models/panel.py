from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords


class Panel(BaseUuidModel):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'getresults'
        ordering = ('name', )
