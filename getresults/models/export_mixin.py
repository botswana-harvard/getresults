from django.db import models


class ExportMixin(models.Model):

    last_exported = models.BooleanField(default=False)

    last_exported_datetime = models.DateTimeField(null=True)

    class _Meta:
        abstract = True
