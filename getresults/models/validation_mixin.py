from django.db import models

from ..choices import VALIDATION_OPTIONS


class ValidationMixin(models.Model):

    validation = models.CharField(
        max_length=1,
        choices=VALIDATION_OPTIONS,
        null=True)

    validation_datetime = models.DateTimeField(null=True)

    validation_user = models.CharField(
        max_length=25,
        null=True)

    class Meta:
        abstract = True
