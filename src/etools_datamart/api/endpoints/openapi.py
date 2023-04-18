# flake8: noqa E501

from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator

description = """
Each API endpoint allows filtering and/or ordering results.
Different formats can be requested using `format` argument`

## Query lookups

### Generic lookups

- exact: Case-sensitive exact match.
- iexact: Case-insensitive exact match.
- contains: Case-sensitive containment test.
- icontains: Case-insensitive containment test.
- in: In a given list.
- gt: Greater than.
- gte: Greater than or equal to.
- lt: Less than.
- lte: Less than or equal to.

### Strings lookups

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

### Negate

- use `!=` operator to negate each value

## Query Examples

Select all interventions in Bolivia and Chad

- {HOST}latest/datamart/interventions/?country_name__in=Bolivia,Chad

Select all interventions in all countries except Bolivia and Zimbabwe

- {HOST}latest/datamart/interventions/?country_name__in!=Bolivia,Zimbabwe (note `!=` instead of `=`)

Select all interventions submitted in 2017

- {HOST}latest/datamart/interventions/?submission_date__year=2017

Select all interventions submitted after 2017 (ie starting 2018)

- {HOST}latest/datamart/interventions/?submission_date__year__gt=2017

Retrieve entries in the second quarter (April 1 to June 30):

- {HOST}latest/datamart/interventions/?submission_date__quarter=2

Retrieve entries in the second/third/fourth quarter (April 1 to June 30):

- {HOST}latest/datamart/interventions/?submission_date__quarter__gte=2


""".format(
    HOST=swagger_settings.DEFAULT_API_URL
)


class DatamartAutoSchema(AutoSchema):
    def _get_operation_id(self, path, method):
        return "a___sss"
        # return super()._get_operation_id(path, method)


class DatamartSchemaGenerator(OpenAPISchemaGenerator):
    pass


schema_view = get_schema_view(
    openapi.Info(
        title="eTools Datamart API",
        default_version="v1",
        description=description,
        # terms_of_service="https://",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
        # aaaaaaa="aaaaaa",
    ),
    generator_class=DatamartSchemaGenerator,
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
