import csv
import os

from django.conf import settings

from ..models import UtestidMapping, Sender, Utestid, Panel


def load_utestidmappings_from_csv(csv_filename=None, header_fields=None):

    def sender(name):
        try:
            return Sender.objects.get(name=name.strip().lower())
        except Sender.DoesNotExist:
            return Sender.objects.create(
                name=name.strip().lower(),
                description=name.strip().lower())

    csv_filename = csv_filename or os.path.join(settings.BASE_DIR, 'testdata/utestid_mappings.csv')
    header_fields = header_fields or ['utestid_name', 'sender', 'sender_utestid_name', 'panel_name']
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f, quotechar="'")
        header = next(reader)
        header = [h.lower() for h in header]
        if header != header_fields:
            raise ValueError(
                'Invalid header. Expected {1}. Got {0}.'.format(','.join(header), ','.join(header_fields)))
        for row in reader:
            r = dict(zip(header, row))
            try:
                panel = Panel.objects.get(name=r['panel_name'].strip().lower())
                utestid = Utestid.objects.get(name=r['utestid_name'].strip().lower())
                UtestidMapping.objects.get(
                    sender=sender(r['sender']),
                    sender_utestid_name=r['sender_utestid_name'].strip().lower(),
                    panel=panel,
                )
            except UtestidMapping.DoesNotExist:
                UtestidMapping.objects.create(
                    sender=sender(r['sender']),
                    utestid=utestid,
                    sender_utestid_name=r['sender_utestid_name'].strip().lower(),
                    panel=panel,
                )
            except (Utestid.DoesNotExist, Panel.DoesNotExist) as e:
                raise ValueError(
                    '{}. Try importing or creating this item before importing this CSV file. Got {}'.format(
                        str(e),
                        {'sender': r['sender'].strip().lower(),
                         'sender_utestid_name': r['sender_utestid_name'].strip().lower(),
                         'utestid_name': r['utestid_name'].strip().lower(),
                         'panel_name': r['panel_name'].strip().lower()
                         }))
