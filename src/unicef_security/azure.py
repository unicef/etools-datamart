import logging

import requests
from constance import config as constance
from crashlog.middleware import process_exception
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from social_django.models import UserSocialAuth

from . import config

AZURE_GRAPH_API_TOKEN_CACHE_KEY = 'azure_graph_api_token_cache_key'
AZURE_GRAPH_DELTA_LINK_KEY = 'azure_graph_delta_link_key'

logger = logging.getLogger(__name__)

DJANGOUSERMAP = {'_pk': ['username'],
                 'username': 'userPrincipalName',
                 'email': 'mail',
                 'azure_id': 'id',
                 'job_title': 'jobTitle',
                 'display_name': 'displayName',
                 'first_name': 'givenName',
                 'last_name': 'surname'}

ADMIN_EMAILS = [i[1] for i in settings.ADMINS]


def default_group(**kwargs):
    is_new = kwargs.get('is_new', False)
    user = kwargs.get('user', None)
    if is_new:
        if user.email in ADMIN_EMAILS:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        else:
            g = Group.objects.filter(name=constance.DEFAULT_GROUP).first()
            if g:
                user.groups.add(g)


def get_unicef_user(backend, details, response, *args, **kwargs):
    from .models import User
    if details.get('email'):
        filters = {'email': details['email']}
    elif details.get('unique_name'):
        filters = {'username': details['unique_name']}
    elif details.get('username'):
        filters = {'username': details['username']}

    try:
        user = User.objects.get(**filters)
        social = user.social_auth
        created = False
    except User.DoesNotExist:
        for k, v in response.items():
            if k in ['email', 'family_name', 'unique_name']:
                details[k] = v
        try:
            sync = Synchronizer()
            data = sync.get_user(details['email'])

            for k, v in data.items():
                details[k] = v

            for k, v in response.items():
                # TODO: remove me
                print(111, f"{k} : {v}")
        except Exception as e:
            process_exception(e)

        user, created = User.objects.get_or_create(
            username=details['unique_name'],
            defaults={'first_name': details.get('givenName', ''),
                      'last_name': details.get('surname', ''),
                      'job_title': details.get('jobTitle', ''),
                      'display_name': details.get('displayName', details['unique_name']),
                      'email': details.get('email', ''),
                      'azure_id': details.get('id'),
                      }
        )
        social, __ = UserSocialAuth.objects.get_or_create(user=user,
                                                          provider=backend.name,
                                                          uid=user.username
                                                          )
    return {'user': user,
            'social': social,
            'is_new': created}


class SyncResult:
    def __init__(self, keep_records=False):
        """
        :param keep_records: if True keep track of record istances
        """
        self.created = []
        self.updated = []
        self.skipped = []
        self.keep_records = keep_records

    def log(self, *result):
        if len(result) == 2:
            obj = {True: result[0],
                   False: result[0].pk}[self.keep_records]
            if result[1]:
                self.created.append(obj)
            else:
                self.updated.append(obj)
        else:
            self.skipped.append(result)

    def __add__(self, other):
        if isinstance(other, SyncResult):
            ret = SyncResult()
            ret.created.extend(other.created)
            ret.updated.extend(other.updated)
            ret.skipped.extend(other.skipped)
            return ret
        else:
            raise ValueError("Cannot add %s to SyncResult object" % type(other))

    def __repr__(self):
        return f"<SyncResult: {len(self.created)} {len(self.updated)} {len(self.skipped)}>"

    def __eq__(self, other):
        if isinstance(other, SyncResult):
            return (self.created == other.created and
                    self.updated == other.updated and
                    self.skipped == other.skipped)
        return False


NotSet = object()


class Synchronizer:
    def __init__(self, user_model=None, mapping=None, echo=None):
        self.user_model = user_model or get_user_model()
        self.field_map = dict(mapping or DJANGOUSERMAP)
        self.user_pk_fields = self.field_map.pop('_pk')
        self._baseurl = '{}/{}/users'.format(config.AZURE_GRAPH_API_BASE_URL,
                                             config.AZURE_GRAPH_API_VERSION)
        self.startUrl = "%s/delta" % self._baseurl
        self.access_token = self.get_token()
        self.next_link = None
        self._delta_link = ''
        self.echo = echo or (lambda l: True)

    def get_token(self):
        if not config.UNICEF_AZURE_CLIENT_ID and config.UNICEF_AZURE_CLIENT_SECRET:
            raise ValueError("Configure AZURE_CLIENT_ID and/or AZURE_CLIENT_SECRET")
        token = cache.get(AZURE_GRAPH_API_TOKEN_CACHE_KEY)
        if not token:
            post_dict = {'grant_type': 'client_credentials',
                         'client_id': config.UNICEF_AZURE_CLIENT_ID,
                         'client_secret': config.UNICEF_AZURE_CLIENT_SECRET,
                         'resource': config.AZURE_GRAPH_API_BASE_URL}
            response = requests.post(config.AZURE_TOKEN_URL, post_dict)
            if response.status_code != 200:  # pragma: no cover
                logger.error(f"Unable to fetch token from Azure. {response.status_code} {response.content}")
                raise Exception(f'Error during token retrieval: {response.status_code} {response.content}')
            jresponse = response.json()
            token = jresponse['access_token']
            # Cache token for 3600 seconds, which matches the default Azure token expiration
            cache.set(AZURE_GRAPH_API_TOKEN_CACHE_KEY, token, 3600)
        return token

    @property
    def delta_link(self):
        return self._delta_link

    @delta_link.setter
    def delta_link(self, value):
        self._delta_link = value

    def get_page(self, url, single=False):
        while True:
            headers = {'Authorization': 'Bearer {}'.format(self.get_token())}
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 401:
                    data = response.json()
                    if data["error"]["message"] == "Access token has expired.":
                        continue
                    else:
                        raise ConnectionError(f'400: Error processing the response {response.content}')

                elif response.status_code != 200:
                    raise ConnectionError(f'Code {response.status_code}. '
                                          f'Error processing the response {response.content}')
                break
            except ConnectionError as e:
                logger.exception(e)
                raise

        jresponse = response.json()
        self.next_link = jresponse.get('@odata.nextLink', None)
        self.delta_link = jresponse.get('@odata.deltaLink', None)
        if single:
            return jresponse
        return jresponse.get('value', [])

    def __iter__(self):
        values = self.get_page(self.startUrl)
        pages = 1
        while True:
            try:
                yield values.pop()
            except IndexError:
                if not self.next_link:
                    logger.debug(f"All pages  fetched. deltaLink: {self.delta_link}")
                    break
                values = self.get_page(self.next_link)
                logger.debug(f"fetched page {pages}")
                pages += 1
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.exception(e)
                break

    def get_record(self, user_info: dict) -> (dict, dict):
        data = {fieldname: user_info.get(mapped_name, '')
                for fieldname, mapped_name in self.field_map.items()}
        pk = {fieldname: data.pop(fieldname) for fieldname in self.user_pk_fields}
        return pk, data

    def fetch_users(self, filter):
        self.startUrl = "%s?$filter=%s" % (self._baseurl, filter)
        return self.syncronize()

    def get_user(self, username):
        url = "%s/%s" % (self._baseurl, username)
        user_info = self.get_page(url, single=True)
        return user_info

    def sync_user(self, user):
        if not user.azure_id:
            raise ValueError("Cannot sync user without azure_id")
        url = "%s/%s" % (self._baseurl, user.azure_id)
        user_info = self.get_page(url, single=True)
        pk, values = self.get_record(user_info)
        user, __ = self.user_model.objects.update_or_create(**pk,
                                                            defaults=values)
        return user

    def resume(self, *, delta_link=None, max_records=None):
        if delta_link:
            self.startUrl = delta_link
        return self.syncronize(max_records)

    def is_valid(self, user_info):
        return (user_info.get('email') and
                user_info.get('first_name') and
                user_info.get('last_name') and
                'noreply' not in user_info.get('email'))

    def syncronize(self, max_records=None):
        logger.debug("Start Azure user synchronization")
        results = SyncResult()
        try:
            for i, user_info in enumerate(iter(self)):
                pk, values = self.get_record(user_info)
                if self.is_valid(values):
                    user_data = self.user_model.objects.update_or_create(**pk,
                                                                         defaults=values)
                    self.echo(user_data)
                    results.log(user_data)
                else:
                    results.log(user_info)
                if max_records and i > max_records:
                    break
        except Exception as e:
            logger.exception(e)
            process_exception(e)
            raise
        logger.debug(f"End Azure user synchronization: {results}")
        return results
