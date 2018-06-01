from django.core.management import call_command
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "_json_imports"))
        data_file = os.path.join(path, "data.json")

        self.stdout.write("LOADING DATABASE FROM THE FOLLOWING FILE:")
        self.stdout.write("\t{0}".format(data_file))

        call_command('loaddata', data_file)
