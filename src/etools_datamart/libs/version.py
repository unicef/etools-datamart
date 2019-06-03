import datetime
import functools
import os
import subprocess

# from distutils.version import LooseVersion


@functools.lru_cache()
def get_git_changeset():
    """Return a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen(
        'git log --pretty=format:%ct --quiet -1 HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=repo_dir, universal_newlines=True,
    )
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:  # pragma: no cover
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


@functools.lru_cache(1)
def get_git_status(clean='', dirty='*'):
    import subprocess
    try:
        uncommited = subprocess.check_output(['git', 'status', '-s'],
                                             stderr=None)
        return dirty if uncommited else clean
    except (subprocess.CalledProcessError, FileNotFoundError):  # pragma: no-cover
        return ''


def get_full_version():  # pragma: no cover
    from etools_datamart import VERSION
    commit = get_git_changeset()
    if commit:
        return f"{VERSION} - {commit} {get_git_status()}"
    return VERSION
#
#
# def get_version_tuple(version):
#     """
#     Return a tuple of version numbers (e.g. (1, 2, 3)) from the version
#     string (e.g. '1.2.3').
#     """
#     loose_version = LooseVersion(version)
#     version_numbers = []
#     for item in loose_version.version:
#         if not isinstance(item, int):
#             break
#         version_numbers.append(item)
#     return tuple(version_numbers)
