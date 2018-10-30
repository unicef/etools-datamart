# -*- coding: utf-8 -*-
# flake8: noqa E501

from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.views import get_schema_view
from rest_framework import permissions

description = """
# Welcome to eTools Datamart API

Each API endpoint allows filtering and/or ordering results.

Fiel
## Query lookups

Any field where query functions are enabled allow to....

### Generic lookups

- exact: Case-sensitive exact match.
- iexact: Case-insensitive exact match.
- contains: Case-sensitive containment test.
- icontains: Case-insensitive containment test.
- inlist: In a given list.
- gt: Greater than.
- gte: Greater than or equal to.
- lt: Less than.
- lte: Less than or equal to.

### String lookups

- startswith: Case-sensitive starts-with.
- istartswith: Case-insensitive starts-with.
- endswith: Case-sensitive ends-with.
- iendswith: Case-insensitive ends-with.
- isnull: null value test.

### Dates

- year: For date and datetime fields, an exact year match. Allows chaining additional field lookups.
- month: An exact month match. Allows chaining additional field lookups. Takes an integer 1 (January) through 12 (December).
- day: An exact day match. Allows chaining additional field lookups. Takes an integer day.
- week: Week number (1-52 or 53) according to ISO-8601, i.e., weeks start on a Monday and the first week contains the year’s first Thursday.
- week_day: ‘day of the week’ match. Allows chaining additional field lookups. Takes an integer value representing the day of week from 1 (Sunday) to 7 (Saturday).
- quarter: ‘quarter of the year’ match. Allows chaining additional field lookups. Takes an integer value between 1 and 4 representing the quarter of the year.

- time
- hour
- minute


- regex
- iregex

### Negate

- not
- not_inlist

## Query Examples

- {HOST}datamart/interventions/?country_name__inlist=Bolivia,Chad

- {HOST}datamart/interventions/?country_name__not_inlist=Bolivia,Zimbabwe

- {HOST}datamart/interventions/?submission_date__year=2017

- {HOST}datamart/interventions/?submission_date__year__gt=2017

- {HOST}datamart/interventions/?submission_date__year__gt=2017

Example to retrieve entries in the second quarter (April 1 to June 30):

- {HOST}datamart/interventions/?submission_date__quarter=2

Example to retrieve entries in the second/third/fourth quarter (April 1 to June 30):

- {HOST}datamart/interventions/?submission_date__quarter__gte=2


""".format(HOST=swagger_settings.DEFAULT_API_URL)

schema_view = get_schema_view(
    openapi.Info(
        title="eTools Datamart API",
        default_version='v1',
        description=description,
        # terms_of_service="https://",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
        # aaaaaaa="aaaaaa",
    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
