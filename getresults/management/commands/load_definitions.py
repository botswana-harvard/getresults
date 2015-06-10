import os
import sys

from unipath import Path

from django.core.management.base import BaseCommand, CommandError

from getresults_csv.utils import load_csv_file
from getresults.utils import load_panels_from_csv, load_utestids_from_csv, load_panel_items_from_csv


class Command(BaseCommand):
    help = 'Load data from a folder containing panels.csv, utestids.csv, panel_items.csv'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for path in options['path']:
            try:
                path = Path(os.path.expanduser(path))
                files = []
                files.append(('panels.csv', load_panels_from_csv))
                files.append(('utestids.csv', load_utestids_from_csv))
                files.append(('panel_items.csv', load_panel_items_from_csv))
                load_csv_file(path, files)
            except (FileNotFoundError, ) as e:
                sys.stdout.write('\n')
                raise CommandError(e)
