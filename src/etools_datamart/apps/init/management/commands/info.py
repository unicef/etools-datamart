from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(f"DATABASES")
        for name, config in settings.DATABASES.items():
            self.stdout.write(f"Connection: {name}")
            for entry in ['NAME', 'HOST', 'PORT']:
                self.stdout.write(f"    {entry}: {config[entry]}")
        self.stdout.write("=" * 80)
        self.stdout.write(f"CACHES")
        for name, config in settings.CACHES.items():
            self.stdout.write(f"Connection: {name}")
            for entry in ['BACKEND', 'LOCATION']:
                self.stdout.write(f"    {entry}: {config[entry]}")
