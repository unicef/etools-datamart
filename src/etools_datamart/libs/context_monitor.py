import logging
import resource
import sys
import time

from django.db import connection, reset_queries
from django.test import override_settings
from django.utils import timezone

import humanfriendly
import sqlparse
from pygments import highlight, lexers
from pygments.formatters.terminal import TerminalFormatter


def get_rss_usage():
    # peak memory usage (bytes on OS X, kilobytes on Linux)
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform in ['linux', 'linux2', 'win32']:
        value = value / 1024
    return value


class monitor:
    def __init__(self, verbosity=0, auto_dump=False, celery_eager=None, title=''):
        # db_level: int
        #   0 = no db
        #   1 = only count
        #   2 = short sql
        #   3 = full sql
        #   4 = explain sql
        self.title = title
        self.auto_dump = auto_dump
        self.verbosity = verbosity
        self.settings = {'DEBUG': False}
        if celery_eager is not None:
            self.settings['CELERY_TASK_ALWAYS_EAGER'] = celery_eager

        self.before = None
        self.start_time = None
        self.queries = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if self.auto_dump:
            self.dump()

    @property
    def elapsedf(self):
        return humanfriendly.format_timespan(self.elapsed)

    @property
    def memoryf(self):
        return humanfriendly.format_size(self.memory_usage)

    def start(self):
        self.before = get_rss_usage()
        self.start_time = time.time()
        self.queries = []
        if self.verbosity > 0:
            reset_queries()
            self.settings['DEBUG'] = True
        self.sett = override_settings(**self.settings)
        self.sett.enable()

    def stop(self):
        self.memory_usage = get_rss_usage() - self.before
        self.end_date = timezone.now()
        self.elapsed = time.time() - self.start_time
        self.felapsed = humanfriendly.format_timespan(self.elapsed)

        if self.verbosity:
            self.sett.disable()
            self.queries = connection.queries

    def dump(self):
        print('\n{0} {1} {0}'.format('=' * 10, self.title))
        if self.verbosity == 1:
            print('Queries: ', len(self.queries))
        else:
            for i, q in enumerate(self.queries, 1):
                fmts = {2: lambda: '%s...' % q['sql'][:100],
                        3: lambda: sqlparse.format(q['sql'], reindent=False, keyword_case='upper'),
                        4: lambda: sqlparse.format(q['sql'], reindent=True, keyword_case='upper'),
                        5: lambda: highlight(q['sql'], lexers.get_lexer_by_name('sql'), TerminalFormatter())}
                if self.verbosity == 9:
                    cursor = connection.cursor()
                    cursor.execute('EXPLAIN %s' % q['sql'])
                    print('%3s) %s %s' % (i, q['time'], fmts[5]()))
                    print('\n'.join(r[0] for r in cursor.fetchall()))
                else:
                    print('%3s) %s %s' % (i, q['time'], fmts[self.verbosity]()))
        print('Elapsed: ', self.elapsedf)
        print('Memory usage: ', self.memoryf)


class set_logging_level:
    def __init__(self, **kwargs):
        self.backup = {}
        self.config = kwargs
        formatter = logging.Formatter('%(levelname)-10s %(asctime)s %(name)s %(funcName)s:%(lineno)d %(message)s',
                                      '%Y-%m-%d %H:%M')
        self.handler = logging.StreamHandler(formatter)
        self.handler.setFormatter(formatter)

    def __enter__(self):
        self.start()
        self.root_level = logging.root.manager.disable
        logging.disable(0)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if exc_type:
            raise exc_type(exc_val)

    def start(self):
        logging.disable(sys.maxsize)

        for name, level in self.config.items():
            logger = logging.getLogger(name)
            self.backup[name] = {'level': logger.level,
                                 'handlers': logger.handlers
                                 }
            logger.setLevel(level)
            for h in logger.handlers:
                logger.removeHandler(h)
            logger.addHandler(self.handler)

    def stop(self):
        logging.disable(self.root_level)
        for name, config in self.backup.items():
            logger = logging.getLogger(name)
            logger.setLevel(config['level'])
            logger.handlers = config['handlers']
