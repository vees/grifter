from django.core.management.base import BaseCommand, CommandError
import eso.imports.load_simple 

class Command(BaseCommand):
	args = '<directory>'
	help = 'Loads all new files from directory'

	def handle(self, *args, **options):
		try:
			print "Started import"
			print eso.imports.load_simple.import_images("")
			print "Done"
		except KeyboardInterrupt:
			print "Interrupted"
			exit
