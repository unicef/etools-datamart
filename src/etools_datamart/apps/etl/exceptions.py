class LoaderException(Exception):
    def __init__(self, message, error=None):  # pragma: no cover
        self.message = message
        self.error = error

    def __repr__(self):
        return str(self.message)


class RequiredIsRunning(Exception):

    def __init__(self, req, *args: object) -> None:
        self.req = req

    def __str__(self):
        return "Required ETL '%s' is running" % str(self.req.loader.etl_task.task)


class RequiredIsMissing(Exception):

    def __init__(self, req, *args: object) -> None:
        self.req = req

    def __str__(self):
        return "Missing required ETL '%s'" % str(self.req.loader.etl_task.task)


class MaxRecordsException(Exception):
    pass
