from django.core.management import call_command
from django.core.management.base import BaseCommand
from spectre.settings import *
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        apps = list(set(INSTALLED_APPS) - set(NON_EXPORT_APPS))
        self.stdout.write("DUMPING DATABASE FOR THE FOLLOWING APPS:")
        self.stdout.write("\t" + " ".join(apps))

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "_json_imports"))
        data_file = os.path.join(path, "data.json")

        with open(data_file, "w+") as f:
            call_command('dumpdata', *apps, stdout=f, indent=2)

        self.stdout.write("Data dumped to {0}".format(data_file))
