from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from .panel import Panel
from .utestid import Utestid


class PanelItem(BaseUuidModel):
    """Model that represents one item in a panel.

    Has methods to format absolute values and to calculate, then format,
    calculated values. Lower and Upper limits of detection determine the
    quantifier.

    For example:
        * If the lower limit of detection is 400, a value of 400 returns ('=', 400)
          and a value of 399 returns ('<', 400).
        * if the upper limit of detection is 750000, a value of 750000 returns ('=', 750000)
          and a value of 750001 returns ('>', 750000)
    """
    panel = models.ForeignKey(Panel)

    utestid = models.ForeignKey(Utestid)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.utestid.name, self.panel.name)

    class Meta:
        app_label = 'getresults'
        unique_together = ('panel', 'utestid')
        ordering = ('panel', 'utestid')
