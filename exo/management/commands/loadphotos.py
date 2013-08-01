from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	args = '<directory>'
	help = 'Loads all new files from directory'

	def handle(self, *args, **options):
		self.stdout.write('Hello world\n')
		self.stdout.write('Hello world\n')

