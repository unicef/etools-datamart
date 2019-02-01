from unittest import mock

from django.urls import reverse

import pytest
from constance.test import override_config
from test_utilities.factories import UserFactory

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSJ9." \
        "eyJhdWQiOiI2ZjU1MDQ1Yi03ZGE5LTQ4ZGYtOTI3Ny1mMmExNzBlNjBkZjAiLCJpc3MiOiJodHRwczovL2xvZ" \
        "2luLm1pY3Jvc29mdG9ubGluZS5jb20vYmVlOWVlMjItNDg3My00NjFiLTgyYTMtY2UyYTUzNmQ3YzYyL3YyLj" \
        "AiLCJpYXQiOjE1Mzk2MTI4OTIsIm5iZiI6MTUzOTYxMjg5MiwiZXhwIjoxNTM5NjE2NzkyLCJhaW8iOiJBVFF" \
        "BeS84SkFBQUEwb3M0VnhzM0NscndOakdrazhWVllaY0tza0JYd1lYS0pCWGhMd0YwRDgwQ1pmMTczWEZwL2Jo" \
        "R1BrUzRDUUFsIiwibmFtZSI6IlJvYmVydCBBdnJhbSIsIm5vbmNlIjoiNWU3YTJjNjMtMDM4Ni00MDY3LTliN" \
        "TAtMTRmMjU1MGEwYTY5Iiwib2lkIjoiYThiYzEyZjgtMDZmNC00MTQ2LTk0MDAtZWYyZjY3NTBlYWE5IiwicH" \
        "JlZmVycmVkX3VzZXJuYW1lIjoicmF2ZGV2QG5pa3VuaWNlZi5vbm1pY3Jvc29mdC5jb20iLCJzdWIiOiJfc1l" \
        "nb2V4OEtwNzdtS0d6Ym9jMHJFbWFaZldaNWxIQ054M2tyaTlNVTA0IiwidGlkIjoiYmVlOWVlMjItNDg3My00" \
        "NjFiLTgyYTMtY2UyYTUzNmQ3YzYyIiwidXRpIjoiV29ERmJ2UW5OVUdCUnFYNXJQblFBQSIsInZlciI6IjIuM" \
        "CJ9.TTlRxiyfkotdnJMhi8Wnw2NtLD-52DPV1kj1Qram2PxCazPKSJcZrwx86DjR7_9a5z9bwAs5EnBiRie2y" \
        "JP-QYRUHOOtiWtca73NG3FMWSMcAi20AiK-BKsWr8aWfbUJFUwHocVvsDn1Hjc1LKUSEruK6IbWe1cKNasU4o" \
        "VDkHa5nWv6fkt2BsH-vtzLYvD2pgryOzhm0YXovW5yjVVYJI9puMuxvLLXYNamSKMrm8kPNGVRbtZjzanvMP1" \
        "lRzgN_Mn4bZsDJJYSaa3JLCr4fz5qUBqhEKS9r1EFldJFx4yoF8UqJslAEoIMFE_baJtt3zTnBJGFB2GeHaD-jwSCeA"


@pytest.fixture()
def user(db):
    return UserFactory(id=-1, username='user1')


def test_token(user, client):
    url = reverse('api:partners-list', args=['v1'])
    client.credentials(HTTP_AUTHORIZATION='jwt ' + TOKEN)
    with mock.patch('unicef_security.graph.Synchronizer.get_user',
                    return_value={'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
                                  'id': '21d2ecba-83e4-4e81-a93c-d44f55dd222e', 'businessPhones': [],
                                  'displayName': 'Stefano Apostolico', 'givenName': 'Stefano', 'jobTitle': None,
                                  'mail': 'sapostolico@unicef.org', 'mobilePhone': None, 'officeLocation': None,
                                  'preferredLanguage': None, 'surname': 'Apostolico',
                                  'userPrincipalName': 'sapostolico@unicef.org'}):
        with mock.patch('rest_framework_jwt.settings.api_settings.JWT_VERIFY_EXPIRATION', False):
            ret = client.get(url)
            assert ret.status_code == 200, ret.json()


@override_config(AZURE_USE_GRAPH=False)
def test_token2(user, client):
    url = reverse('api:partners-list', args=['v1'])
    client.credentials(HTTP_AUTHORIZATION='jwt ' + TOKEN)
    with mock.patch('rest_framework_jwt.settings.api_settings.JWT_VERIFY_EXPIRATION', False):
        ret = client.get(url)
        assert ret.status_code == 200, ret.json()
