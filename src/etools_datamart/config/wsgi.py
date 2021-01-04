import os

from django.core.wsgi import get_wsgi_application

from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etools_datamart.config.settings")

application = Cling(get_wsgi_application())
# application = WhiteNoise(get_wsgi_application(), root=os.environ.get('STATIC_ROOT'))
# application.add_files('/path/to/more/static/files', prefix='more-files/')
