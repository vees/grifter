from django.core.management.base import BaseCommand, CommandError
import eso.sync.exclude_list

class Command(BaseCommand):
    args = '<directory>'
    help = 'Loads all new files from directory'

    def handle(self, *args, **options):
        eso.sync.exclude_list.main()
