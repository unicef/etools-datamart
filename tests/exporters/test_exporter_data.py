# import pytest
# from rest_framework.test import APIClient
#
# @pytest.fixture()
# def client(admin_user):
#     client = APIClient()
#     assert client.login(username='admin', password='password')
#     return client
#
#
# @pytest.mark.skipif(os.environ.get("CIRCLECI") == "true", reason="Skip in CirlceCI")
# def test_export_azure_data(db, client, settings):
#     UserStats.loader.unlock()
#     UserStats.loader.load()
#     assert UserStats.objects.count()
#
#     url = reverse("api:userstats-list", args=['v1'])
#     res = client.get(f"{url}?format=xlsx")
#
#     from storages.backends.azure_storage import AzureStorage
#     storage = AzureStorage()
#     storage.save('test1.xlsx', io.BytesIO(res.content))
