from django.db.models import Q

from etools_datamart.apps.mart.data.models.location import GeoName, GeoNameLimitException
from etools_datamart.celery import app


@app.task
def update_geonames():
    # update those geonames that are missing data
    for geoname in GeoName.objects.filter(Q(name__isnull=True) | Q(name="")):
        try:
            geoname.sync()
        except GeoNameLimitException:
            break  # have reached our daily limit, so pointless continuing
