import base64
import json
import logging
import os

import requests
from constance import config as constance
from crashlog.middleware import process_exception
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from jwt import decode as jwt_decode, DecodeError, ExpiredSignature
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.exceptions import AuthTokenError
from social_django.models import UserSocialAuth
from unicef_security.config import GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET

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


class AzureADTenantOAuth2Ext(AzureADTenantOAuth2):
    def user_data(self, access_token, *args, **kwargs):
        response = kwargs.get('response')
        id_token = response.get('id_token')

        # decode the JWT header as JSON dict
        jwt_header = json.loads(
            base64.b64decode(id_token.split('.', 1)[0]).decode()
        )

        # get key id and algorithm
        key_id = jwt_header['kid']
        algorithm = jwt_header['alg']
        verify = os.environ.get('OAUTH2_VERIFY', False)
        key = ''
        try:
            # retrieve certificate for key_id
            if verify:
                certificate = self.get_certificate(key_id)
                key = certificate.public_key()

            return jwt_decode(
                id_token,
                verify=verify,
                key=key,
                algorithms=algorithm,
                audience=self.setting('KEY')
            )
        except (DecodeError, ExpiredSignature) as error:
            raise AuthTokenError(self, error)


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
        social = user.social_auth.get()
        user.social_user = social
        created = False
    except (User.DoesNotExist, UserSocialAuth.DoesNotExist):
        for k, v in response.items():
            if k in ['email', 'family_name', 'unique_name']:
                details[k] = v
        try:
            sync = Synchronizer()
            data = sync.get_user(details['email'])

            for k, v in data.items():
                details[k] = v

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
        user.social_user = social
    return {'user': user,
            'social': social,
            'uid': details.get('id'),
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
    def __init__(self, user_model=None, mapping=None, echo=None, id=None, secret=None):
        self.id = id or GRAPH_CLIENT_ID
        self.secret = secret or GRAPH_CLIENT_SECRET

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
        if not self.id and self.secret:
            raise ValueError("Configure AZURE_CLIENT_ID and/or AZURE_CLIENT_SECRET")
        token = cache.get(AZURE_GRAPH_API_TOKEN_CACHE_KEY)
        if not token:
            post_dict = {'grant_type': 'client_credentials',
                         'client_id': self.id,
                         'client_secret': self.secret,
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

    def fetch_users(self, filter, callback=None):
        self.startUrl = "%s?$filter=%s" % (self._baseurl, filter)
        return self.syncronize(callback=callback)

    def search_users(self, record):
        url = "%s?$filter=" % self._baseurl
        filters = []
        if record.email:
            filters.append("mail eq '%s'" % record.email)
        if record.last_name:
            filters.append("surname eq '%s'" % record.last_name)
        if record.first_name:
            filters.append("givenName eq '%s'" % record.first_name)

        page = self.get_page(url + " or ".join(filters), single=True)
        return page['value']

    def filter_users_by_email(self, email):
        """https://graph.microsoft.com/v1.0/users?$filter=mail eq 'sapostolico@unicef.org'"""
        url = "%s?$filter=mail eq '%s'" % (self._baseurl, email)
        page = self.get_page(url, single=True)
        return page['value']

    def get_user(self, username):
        url = "%s/%s" % (self._baseurl, username)
        user_info = self.get_page(url, single=True)
        return user_info

    def sync_user(self, user, azure_id=None):
        if not (azure_id or user.azure_id):
            raise ValueError("Cannot sync user without azure_id")
        url = "%s/%s" % (self._baseurl, azure_id or user.azure_id)
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
        return user_info.get('email')

    def syncronize(self, max_records=None, callback=None):
        logger.debug("Start Azure user synchronization")
        results = SyncResult()
        try:
            for i, user_info in enumerate(iter(self)):
                pk, values = self.get_record(user_info)
                if self.is_valid(values):
                    user, created = self.user_model.objects.update_or_create(**pk,
                                                                             defaults=values)
                    if callback:
                        callback(user=user, is_new=created)
                    self.echo([user, created])
                    results.log(user, created)
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
