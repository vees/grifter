from django.core.management.base import BaseCommand, CommandError
import eso.sync.exclude_list

class Command(BaseCommand):
    args = ''
    help = 'Print a list of files excluded based on private=True'

    def handle(self, *args, **options):
        eso.sync.exclude_list.main()
