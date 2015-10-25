from django.core.management.base import BaseCommand, CommandError

from getresults.configure import Configure


class Command(BaseCommand):
    help = 'Load data from a folder containing panels.csv, utestids.csv, panel_items.csv'

    def handle(self, *args, **options):
        print('Running configure ...')
        configure = Configure()
        configure.load_all()
        print('Done')
