#!/usr/bin/env python
import os
import sys
import warnings

from django.core.management import execute_from_command_line

warnings.simplefilter("ignore", UserWarning, 144)

ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.realpath(os.path.join(ROOT, 'src'))
sys.path.append(SRC)

if __name__ == '__main__':
    settings_file = 'etools_datamart.config.settings._%s' % os.environ.get('USER', "")
    if not os.path.isfile(settings_file):
        settings_file = 'etools_datamart.config.settings'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)
    import logging

    logger = logging.getLogger('raven.contrib.django.client.DjangoClient')

    # from django.core.management import execute_from_command_line

    debug_on_error = '--pdb' in sys.argv
    args = [a for a in sys.argv if a != '--pdb']

    try:
        execute_from_command_line(args)
    except Exception:
        if debug_on_error:
            import pdb, traceback  # noqa

            __, __, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
        else:
            raise
