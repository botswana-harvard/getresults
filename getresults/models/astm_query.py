from django.db import models
from django.utils import timezone


class AstmQuery(models.Model):

    patient_identifier = models.CharField(
        max_length=16,
    )

    aliquot_identifier = models.CharField(
        max_length=16,
    )

    query_datetime = models.DateTimeField(
        default=timezone.now
    )

    sent = models.BooleanField(
        default=False)

    class Meta:
        app_label = 'getresults'
