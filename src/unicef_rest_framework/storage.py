import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.deconstruct import deconstructible

from redis import Redis
from storages.backends.azure_storage import AzureStorage
from storages.utils import setting


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


# from .file import RedisFile

class RedisFile(object):
    def __init__(self, redis_key, redis_connection=None):
        # Force self.buf to be a string or unicode
        self.buf = None
        self.len = 0
        self.buflist = []
        self.pos = 0
        self.closed = False
        self.softspace = 0
        # You can passin an existing redis connection for
        # connection pooling.
        if redis_connection:
            self.redis = redis_connection
        self.redis_key = redis_key

    def _complain_ifclosed(self):
        if self.closed:
            raise ValueError("I/O operation on closed file")

    def isatty(self):
        self._complain_ifclosed()
        return False

    def flush(self):
        self._complain_ifclosed()
        pass

    def write(self, s):
        self._complain_ifclosed()
        self.redis.rpush(self.redis_key, s)

    def writelines(self, s):
        self._complain_ifclosed()
        if isinstance(s, str):
            s = s.split('\n')
        self.redis.rpush(self.redis_key, *s)

    def next(self):
        self._complain_ifclosed()
        r = self.readline()
        if not r:
            raise StopIteration
        return r

    def read(self):
        self._complain_ifclosed()
        return b"".join(self.readlines())

    def readline(self):
        self._complain_ifclosed()
        try:
            data = self.redis.lrange(self.redis_key, self.pos, self.pos)[0]
            # data = data + b'\n'
        except IndexError:
            return None
        self.pos += 1
        return data

    def readlines(self):
        self._complain_ifclosed()
        data = self.redis.lrange(self.redis_key, self.pos, -1)
        self.pos += len(data)
        return data

    def seek(self, s):
        self._complain_ifclosed()
        self.pos = s

    def close(self):
        self.closed = True

    def __str__(self):
        return "%s" % self.__dict__

    def __iter__(self):
        while True:
            line = self.readline()
            if line:
                yield line
            else:
                raise StopIteration


class RedisStorage(Storage):
    _redis_connection = None

    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self._redis_connection = Redis(host, port, db, password)

    def _open(self, name, *args, **kwargs):
        return RedisFile(name, redis_connection=self._redis_connection)

    def _save(self, name, content):
        redis_file = RedisFile(name, redis_connection=self._redis_connection)
        redis_file.writelines(content)
        return name

    def get_valid_name(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        return name

    def url(self, name):
        return u''

    def exists(self, name):
        return self._redis_connection.exists(name)

    def delete(self, name):
        self._redis_connection.delete(name)


@deconstructible
class UnicefAzureStorage(AzureStorage):
    # override defaults
    upload_max_conn = setting("AZURE_UPLOAD_MAX_CONN", 2)
    timeout = setting('AZURE_CONNECTION_TIMEOUT_SECS', 300)

    # new values
    auto_sign = setting("AZURE_AUTO_SIGN")
    access_mode = setting("AZURE_ACCESS_MODE")
    access_ttl = setting("AZURE_ACCESS_TTL")

    def __init__(self, *args, **kwargs):
        super().__init__()

    def url(self, name, expire=None):
        if hasattr(self.service, 'make_blob_url'):
            if self.auto_sign:
                start = (datetime.utcnow() + timedelta(seconds=-120)).strftime('%Y-%m-%dT%H:%M:%SZ')
                expiry = (datetime.utcnow() + timedelta(seconds=self.access_ttl)).strftime('%Y-%m-%dT%H:%M:%SZ')
                sas_token = self.service.generate_blob_shared_access_signature(
                    self.azure_container,
                    name,
                    permission=self.access_mode,
                    expiry=expiry,
                    start=start,
                )
            else:
                sas_token = None
            return self.service.make_blob_url(
                container_name=self.azure_container,
                blob_name=name,
                protocol=self.azure_protocol,
                sas_token=sas_token,
            )
        else:
            return "{}{}/{}".format(setting('MEDIA_URL'), self.azure_container, name)
