from django.core.management.base import BaseCommand, CommandError
from eso.imports import card_dump

class Command(BaseCommand):
	args = '<directory>'
	help = 'Loads all new files from directory'

	def handle(self, *args, **options):
        card_dump.main()
