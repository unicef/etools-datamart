def strfelapsed(seconds):
    # seconds = 9.888888888888886 * 60 * 60
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)
