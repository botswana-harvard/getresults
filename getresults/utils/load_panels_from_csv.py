import csv
import os

from django.conf import settings

from getresults_order.models import OrderPanel


def load_panels_from_csv(csv_filename=None):
    csv_filename = csv_filename or os.path.join(settings.BASE_DIR, 'testdata/panels.csv')
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f, quotechar="'")
        header = next(reader)
        header = [h.lower() for h in header]
        for row in reader:
            r = dict(zip(header, row))
            try:
                OrderPanel.objects.get(name=r['panel'].strip().lower())
            except OrderPanel.DoesNotExist:
                OrderPanel.objects.create(name=r['panel'].strip().lower())
