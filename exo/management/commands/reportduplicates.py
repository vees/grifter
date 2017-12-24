from django.core.management.base import BaseCommand, CommandError
import eso.imports.load_masterfile 

class Command(BaseCommand):
	args = '<directory>'
	help = 'Loads all new files from directory'

	def handle(self, *args, **options):
		try:
			print("Started duplicates check")
			eso.imports.load_masterfile.report_duplicates_2()
		except KeyboardInterrupt:
			print("Interrupted")
			exit
