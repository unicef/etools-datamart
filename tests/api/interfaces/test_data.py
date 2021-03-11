import os

from drf_api_checker.pytest import contract, frozenfixture
from drf_api_checker.recorder import Recorder
from rest_framework.test import APIClient
from test_utilities.factories import factories_registry, UserFactory

from etools_datamart.api.urls import router


class MyRecorder(Recorder):
    @property
    def client(self):
        user = UserFactory(is_superuser=True)
        client = APIClient()
        client.force_authenticate(user)
        return client


# def frozenfixture2(use_request=False):
#     def deco(func):
#         from drf_api_checker.utils import load_fixtures, dump_fixtures
#         from drf_api_checker.fs import mktree
#
#         @wraps(func)
#         def _inner(*args, **kwargs):
#             parts = [os.path.dirname(func.__code__.co_filename),
#                      BASE_DATADIR,
#                      func.__module__,
#                      func.__name__, ]
#             if 'request' in kwargs:
#                 request = kwargs['request']
#                 viewset = request.getfixturevalue('viewset')
#                 parts.append(viewset.__name__)
#
#             destination = os.path.join(*parts
#                                        ) + '.fixture.json'
#             if os.path.exists(destination) and not os.environ.get('API_CHECKER_RESET'):
#                 return load_fixtures(destination)[func.__name__]
#             mktree(os.path.dirname(destination))
#             data = func(*args, **kwargs)
#             dump_fixtures({func.__name__: data}, destination)
#             return data
#
#         return pytest.fixture(_inner)
#
#     return deco


def pytest_generate_tests(metafunc, *args):
    if 'viewset' in metafunc.fixturenames:
        params = []
        ids = []
        for prefix, viewset, basenametry in router.registry:
            if prefix.startswith('datamart/rapidpro/'):
                pass
            elif prefix.startswith('datamart/'):
                sers = viewset.serializers_fieldsets.keys()
                if sers:
                    for ser in sers:
                        params.append([viewset, ser])
                        ids.append(f'{viewset.__name__}-{ser}')
                else:
                    params.append([viewset, 'std'])
                    ids.append(f'{viewset.__name__}-std')
                # params.append(viewset)
                # ids.append(f'{viewset.__name__}')
        metafunc.parametrize("viewset,serializer", params, ids=ids)


def url(request):
    return ""


def aaaa(seed, request):
    viewset = request.getfixturevalue('viewset')
    url = viewset.get_service().endpoint.strip('.').replace('/', '_')
    return os.path.join(seed, url) + '.fixture.json'


@frozenfixture(fixture_name=aaaa)
def data(db, request):
    # TIPS: database access is forbidden in pytest_generate_tests
    viewset = request.getfixturevalue('viewset')
    factory = factories_registry[viewset.serializer_class.Meta.model]
    data = (factory(schema_name='bolivia'),
            factory(schema_name='chad'),
            factory(schema_name='lebanon'))
    return data


@contract(recorder_class=MyRecorder)
def test_list(request, viewset, serializer, data):
    url = f"{viewset.get_service().endpoint}"
    return [url, {'-serializer': serializer}]


@frozenfixture(fixture_name=aaaa)
def record(db, request):
    # TIPS: database access is forbidden in pytest_generate_tests
    viewset = request.getfixturevalue('viewset')
    factory = factories_registry[viewset.serializer_class.Meta.model]
    return factory(schema_name='bolivia')


@contract(recorder_class=MyRecorder)
def test_record(request, viewset, serializer, record):
    url = f"{viewset.get_service().endpoint}{record.pk}/"
    return url
