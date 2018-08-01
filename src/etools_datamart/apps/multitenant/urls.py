from django.urls import path

from etools_datamart.apps.multitenant.views import SelectSchema

app_name = 'multitenant'

urlpatterns = [
    path(r'', SelectSchema.as_view(), name='select-schema'),
]
