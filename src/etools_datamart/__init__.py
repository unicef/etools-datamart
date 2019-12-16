import warnings

NAME = 'etools-datamart'
VERSION = __version__ = '2.10.0a10'
__author__ = ''

# UserWarning: The psycopg2 wheel package will be renamed from release 2.10.0a10;
warnings.simplefilter("ignore", UserWarning, 144)
