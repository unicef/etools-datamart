import warnings

NAME = 'etools-datamart'
VERSION = __version__ = '1.23.0a4'
__author__ = ''

# UserWarning: The psycopg2 wheel package will be renamed from release 2.8;
warnings.simplefilter("ignore", UserWarning, 144)
