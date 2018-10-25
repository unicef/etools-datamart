from django_countries.fields import CountryField
from unicef_security.models import AbstractBusinessArea


class DatamartBusinessArea(AbstractBusinessArea):
    country = CountryField()

    class Meta:
        app_label = 'security'
