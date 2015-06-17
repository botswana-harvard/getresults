from django.db import models

from getresults.models import Utestid, Panel
from edc_base.model.models import BaseUuidModel, HistoricalRecords

from .sender import Sender


class UtestidMapping(BaseUuidModel):

    sender = models.ForeignKey(Sender)

    panel = models.ForeignKey(Panel)

    utestid = models.ForeignKey(Utestid)

    sender_utestid_name = models.CharField(
        max_length=10)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.sender.name, self.sender_utestid_name)

    class Meta:
        app_label = 'getresults'
        db_table = 'getresults_utestidmapping'
