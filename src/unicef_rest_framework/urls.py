from django.contrib import admin
from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from unicef_rest_framework.views import ExportCreate, ExportFetch, ExportList, ExportUpdate

from .routers import APIRouter

admin.autodiscover()

router = APIRouter()

app_name = "urf"

urlpatterns = (
    path(r"api-token-auth/", obtain_jwt_token),
    path(r"api-token-refresh/", refresh_jwt_token),
    path(r"api-token-verify/", verify_jwt_token),
    path(r"exports/", ExportList.as_view(), name="export-list"),
    path(r"exports/<int:pk>/", ExportUpdate.as_view(), name="export-update"),
    path(r"exports/book/", ExportCreate.as_view(), name="export-create"),
    path(r"exports/fetch/<int:pk>/", ExportFetch.as_view(), name="export-fetch"),
)
