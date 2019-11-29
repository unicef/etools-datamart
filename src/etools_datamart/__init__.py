import warnings

NAME = 'etools-datamart'
VERSION = __version__ = '2.9.0a14'
__author__ = ''

# UserWarning: The psycopg2 wheel package will be renamed from release 2.9.0a14;
warnings.simplefilter("ignore", UserWarning, 144)
