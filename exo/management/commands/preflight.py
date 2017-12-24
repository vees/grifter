from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

'''Check for required configuration variables'''
class Command(BaseCommand):
    def all_in_list(self, list):
        for item in list:
            if not hasattr(settings, item):
                return False
        return True
                
    def handle(self, *args, **options):
        required_list = ["NARTHEX_PHOTO_PATH", "NARTHEX_INSTANCE", "NARTHEX_DEBUG_IMPORT", "NARTHEX_CONTAINER_ID"]
        if not self.all_in_list(required_list):
            print("Required fields missing")
            print(settings.NARTHEX_PHOTO_PATH)
        else:
            print("Required fields present")




