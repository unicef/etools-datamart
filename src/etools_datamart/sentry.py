import sentry_sdk


def process_exception(exception, request=None, message_user=False):
    with sentry_sdk.push_scope() as scope:
        if request:
            scope.set_extra("request", request)
        sentry_sdk.capture_exception(exception)
    pass
