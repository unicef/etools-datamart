from datetime import datetime

from django.db import models

from month_field.models import MonthField

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuthUser


class UserStatsLoader(EtoolsLoader):
    """
    --
    SELECT "users_country"."id",
           "users_country"."schema_name",
           "users_country"."name",
           "users_country"."business_area_code",
           "users_country"."initial_zoom",
           "users_country"."latitude",
           "users_country"."longitude",
           "users_country"."country_short_code",
           "users_country"."vision_sync_enabled",
           "users_country"."vision_last_synced",
           "users_country"."local_currency_id",
           "users_country"."long_name",
           "users_country"."iso3_code",
           "users_country"."custom_dashboards"
    FROM "users_country"
    WHERE NOT ("users_country"."schema_name" IN ('public'))
    ORDER BY "users_country"."name" ASC;

    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count" --
    FROM "auth_user" INNER JOIN "users_userprofile" ON ("auth_user"."id" = "users_userprofile"."user_id")
    WHERE "users_userprofile"."country_id" IN (## List  of "users_country"."id" in the page ##);

    --
    SELECT COUNT(*) AS "__count"
    FROM "auth_user" INNER JOIN "users_userprofile" ON ("auth_user"."id" = "users_userprofile"."user_id")
    WHERE ("users_userprofile"."country_id" IN (## List of "users_country"."id" in the page ##)
    AND "auth_user"."email"::text LIKE '%@unicef.org');

    --
    SELECT COUNT(*) AS "__count"
    FROM "auth_user" INNER JOIN "users_userprofile" ON ("auth_user"."id" = "users_userprofile"."user_id")
    WHERE ("users_userprofile"."country_id" IN (## List of "users_country"."id" in the page ##)
    AND EXTRACT(MONTH FROM "auth_user"."last_login" AT TIME ZONE 'UTC') = 1) ;

    --
    SELECT COUNT(*) AS "__count"
    FROM "auth_user" INNER JOIN "users_userprofile" ON ("auth_user"."id" = "users_userprofile"."user_id")
    WHERE ("users_userprofile"."country_id" IN (## List of "users_country"."id" in the page ##)
    AND "auth_user"."email"::text LIKE '%@unicef.org'
    AND EXTRACT(MONTH FROM "auth_user"."last_login" AT TIME ZONE 'UTC') = 1)
    """

    def get_queryset(self):
        return self.config.source.objects.filter(profile__country=self.context["country"])
        # return AuthUser.objects.filter(profile__country=self.context['country'])

    def update_context(self, **kwargs):
        super().update_context(**kwargs)
        today = self.context["today"]
        self.context.update(first_of_month=datetime(today.year, today.month, 1))
        return self.context

    def process_country(self):
        country = self.context["country"]
        first_of_month = self.context["first_of_month"]
        # base = AuthUser.objects.filter(profile__country=country)
        base = self.get_queryset()
        values = {
            "total": base.count(),
            "unicef": base.filter(email__endswith="@unicef.org").count(),
            "logins": base.filter(last_login__month=first_of_month.month).count(),
            "unicef_logins": base.filter(last_login__month=first_of_month.month, email__endswith="@unicef.org").count(),
            "seen": self.context["today"],
        }
        op = self.process_record(
            filters=dict(
                month=first_of_month,
                country_name=country.name,
                schema_name=country.schema_name,
            ),
            values=values,
        )
        self.increment_counter(op)


class UserStats(EtoolsDataMartModel):
    month = MonthField("Month Value")
    total = models.IntegerField("Total users", default=0)
    unicef = models.IntegerField("UNICEF uswers", default=0)
    logins = models.IntegerField("Number of logins", default=0)
    unicef_logins = models.IntegerField("Number of UNICEF logins", default=0)

    class Meta:
        ordering = ("-month", "country_name")
        unique_together = ("country_name", "month")
        verbose_name = "User Access Statistics"

    loader = UserStatsLoader()

    class Options:
        source = AuthUser
        sync_deleted_records = lambda loader: False
        truncate = True
