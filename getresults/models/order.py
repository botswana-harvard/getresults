from django.db import models

from .panel import Panel


class Order(models.Model):

    order_identifier = models.CharField(
        max_length=50,
        unique=True,
    )

    order_datetime = models.DateTimeField(null=True)

    panel = models.ForeignKey(Panel)

    specimen_identifier = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return '{}: {}'.format(self.order_identifier, self.panel)

    class Meta:
        app_label = 'getresults'
        ordering = ('order_identifier', )
