class LoaderException(Exception):
    def __init__(self, message, error=None):  # pragma: no cover
        self.message = message
        self.error = error

    def __repr__(self):
        return str(self.message)
