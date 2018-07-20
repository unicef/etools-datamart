from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        call_command('migrate', verbosity=verbosity - 1)
        ModelUser = get_user_model()
        if settings.DEBUG:
            pwd = '123'
        else:
            pwd = ModelUser.objects.make_random_password()

        ModelUser.objects.get_or_create(
            username='sax',
            defaults=dict(
                is_superuser=True, is_staff=True, password=make_password(pwd)))
        self.stdout.write(
            "Created superuser `sax` with password `{}`".format(pwd))
