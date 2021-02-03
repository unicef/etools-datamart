import warnings

NAME = 'etools-datamart'
VERSION = __version__ = '3.2'
__author__ = ''

# UserWarning: The psycopg2 wheel package will be renamed from release 2.11;
warnings.simplefilter("ignore", UserWarning, 144)
