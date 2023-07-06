from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuthUser, PartnersPartnerorganization, UsersRealm


class PartnerStaffMemberLoader(EtoolsLoader):
    def process_country(self):
        for partner in PartnersPartnerorganization.objects.all().select_related("organization"):
            for user_realm in UsersRealm.objects.filter(
                country=self.context["country"], organization=partner.organization, group__name__startswith="IP "
            ).select_related("user", "user__profile"):
                filters = self.config.key(self, user_realm.user)
                values = self.get_values(user_realm.user)
                values["source_id"] = user_realm.user.id
                values["user"] = "{0.last_name} {0.first_name} ({0.email})".format(user_realm.user)
                values["phone"] = user_realm.user.profile.phone_number
                values["title"] = user_realm.user.profile.job_title
                values["partner"] = partner.organization.name
                values["partner_id"] = partner.id
                values["vendor_number"] = partner.organization.vendor_number
                values["active"] = user_realm.is_active
                print(values)
                op = self.process_record(filters, values)
                self.increment_counter(op)


class PartnerStaffMember(EtoolsDataMartModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    vendor_number = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)

    loader = PartnerStaffMemberLoader()

    class Options:
        source = AuthUser
