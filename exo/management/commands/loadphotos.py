'''
Example usage:
(env) rob@progress:~/Projects/narthex$ python3 manage.py \
    loadphotos /home/rob/Pictures/2017family/
'''
from django.core.management.base import BaseCommand, CommandError
import eso.imports.local_import

class Command(BaseCommand):
    help = 'Loads all new files from directory'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+')

    def handle(self, *args, **options):
        for path in options['path']:
            try:
                eso.imports.local_import.load_dir(path)
            except KeyboardInterrupt:
                    self.stdout.write('Interruped by user')
            except:
                raise CommandError('Path "%s" did not import' % poll_id)
            self.stdout.write(self.style.SUCCESS(
                'Successfully import path "%s"' % path))
