from etools_datamart.apps.sources.etools.models import (
    PartnersAgreement,
    PartnersAgreementamendment,
    PartnersAgreementAuthorizedOfficers,
    PartnersPartnerstaffmember,
)

from .utils import add_m2m


def reference_number(self):
    return "{code}/{type}{year}{id}".format(
        code=self.get_country_instance().country_short_code or "",
        type=self.agreement_type,
        year=self.reference_number_year,
        id=self.id,
    )


def get_amendments(self):
    return PartnersAgreementamendment.objects.filter(agreement=self)


def get_base_number(self):
    return self.agreement_number.split("-")[0]


PartnersAgreement.reference_number = property(reference_number)
PartnersAgreement.amendments = property(get_amendments)
PartnersAgreement.base_number = property(get_base_number)

add_m2m(
    PartnersAgreement,
    "authorized_officers",
    PartnersPartnerstaffmember,
    through=PartnersAgreementAuthorizedOfficers,
    related_name="agreement_authorizations",
)
