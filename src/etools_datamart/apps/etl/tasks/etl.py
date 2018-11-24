# -*- coding: utf-8 -*-
import json
import logging
from datetime import date, datetime

from django.db import connections
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from strategy_field.utils import get_attr

from etools_datamart.apps.data.models import HACT, Intervention, PMPIndicators
from etools_datamart.apps.data.models.fam import FAMIndicator
from etools_datamart.apps.data.models.user import UserStats
from etools_datamart.apps.etools.models import (AuditAudit, AuditEngagement, AuditMicroassessment,
                                                AuditSpecialaudit, AuditSpotcheck, AuthUser, HactAggregatehact,
                                                PartnersIntervention, PartnersPartnerorganization,)
from etools_datamart.celery import app

logger = logging.getLogger(__name__)

__all__ = ["load_hact", "load_user_report", "load_fam_indicator",
           "load_pmp_indicator", "load_intervention"]

CREATED = 'created'
UPDATED = 'updated'
UNCHANGED = 'unchanged'


class EtlResult:
    __slots__ = [CREATED, UPDATED, UNCHANGED]

    def __init__(self, updated=0, created=0, unchanged=0):
        self.created = created
        self.updated = updated
        self.unchanged = unchanged

    def __repr__(self):
        return repr(self.as_dict())

    def incr(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)

    def as_dict(self):
        return {'created': self.created,
                'updated': self.updated,
                'unchanged': self.unchanged}

    def __eq__(self, other):
        if isinstance(other, EtlResult):
            other = other.as_dict()

        if isinstance(other, dict):
            return (self.created == other['created'] and
                    self.updated == other['updated'] and
                    self.unchanged == other['unchanged'])
        return False


def is_record_changed(record, values):
    other = type(record)(**values)
    for field_name, field_value in values.items():
        if getattr(record, field_name) != getattr(other, field_name):
            return True
    return False


def process(Model, filters, values):
    existing, created = Model.objects.get_or_create(**filters,
                                                    defaults=values)
    if created:
        op = CREATED
    else:
        if is_record_changed(existing, values):
            op = UPDATED
            Model.objects.update_or_create(**filters,
                                           defaults=values)
        else:
            op = UNCHANGED
    return op


@app.etl(HACT)
def load_hact():
    connection = connections['etools']
    countries = connection.get_tenants()
    today = timezone.now()
    results = EtlResult()
    for country in countries:
        connection.set_schemas([country.schema_name])

        logger.info(u'Running on %s' % country.name)
        aggregate = HactAggregatehact.objects.get(year=today.year)
        data = json.loads(aggregate.partner_values)

        # PartnersPartnerorganization.objects.hact_active()
        # qs = PartnersPartnerorganization.objects.filter(Q(reported_cy__gt=0) | Q(total_ct_cy__gt=0), hidden=False)
        # values = dict(microassessments_total=0,
        #               programmaticvisits_total=0,
        #               followup_spotcheck=0,
        #               completed_hact_audits=0,
        #               completed_special_audits=0,
        #               )
        # for partner in qs.all():
        #     values['microassessments_total'] += AuditEngagement.objects.filter(
        #         engagement_type=AuditEngagement.TYPE_MICRO_ASSESSMENT,
        #         status=AuditEngagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year).count()
        #
        #     values['programmaticvisits_total'] += partner.hact_values['programmatic_visits']['completed']['total']
        #     values['followup_spotcheck'] = qs.aggregate(total=Coalesce(Sum(
        #         'planned_engagement__spot_check_follow_up'), 0))['total']
        #
        #     # completed_hact_audits = ?
        #     values['completed_special_audits'] += AuditEngagement.objects.filter(
        #         engagement_type=AuditEngagement.TYPE_SPECIAL_AUDIT,
        #         status=AuditEngagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year).count()

        # # Total number of completed Microassessments in the business area in the past year
        values = dict(microassessments_total=data['assurance_activities']['micro_assessment'],
                      programmaticvisits_total=data['assurance_activities']['programmatic_visits']['completed'],
                      followup_spotcheck=data['assurance_activities']['spot_checks']['follow_up'],
                      completed_spotcheck=data['assurance_activities']['spot_checks']['completed'],
                      completed_hact_audits=data['assurance_activities']['scheduled_audit'],
                      completed_special_audits=data['assurance_activities']['special_audit'],
                      )
        op = process(HACT, filters=dict(year=today.year,
                                        country_name=country.name,
                                        schema_name=country.schema_name),
                     values=values)
        results.incr(op)
        # existing, created = HACT.objects.get_or_create(year=today.year,
        #                                                country_name=country.name,
        #                                                schema_name=country.schema_name,
        #                                                defaults=values)
        # if created:
        #     results.created += 1
        # else:
        #     if is_record_changed(existing, values):
        #         results.updated += 1
        #         HACT.objects.update_or_create(year=today.year,
        #                                       country_name=country.name,
        #                                       schema_name=country.schema_name,
        #                                       defaults=values)
        #     else:
        #         results.unchanged += 1

    return results.as_dict()


@app.etl(PMPIndicators)
def load_pmp_indicator():
    connection = connections['etools']
    countries = connection.get_tenants()
    base_url = 'https://etools.unicef.org'
    results = EtlResult()

    for country in countries:
        connection.set_schemas([country.schema_name])

        logger.info(u'Running on %s' % country.name)
        for partner in PartnersPartnerorganization.objects.all():
            for intervention in PartnersIntervention.objects.filter(agreement__partner=partner):
                planned_budget = getattr(intervention,
                                         'partnersintervention_partners_interventionbudget_intervention_id', None)
                fr_currencies = intervention.frs.all().values_list('currency', flat=True).distinct()
                has_assessment = bool(getattr(partner.current_core_value_assessment, 'assessment', False))
                values = {'country_name': country.name,
                          'schema_name': country.schema_name,
                          'business_area_code': country.business_area_code,
                          'partner_name': partner.name,
                          'partner_type': partner.cso_type,
                          'vendor_number': partner.vendor_number,

                          'pd_ssfa_ref': intervention.number.replace(',', '-'),
                          'pd_ssfa_status': intervention.status.title(),
                          'pd_ssfa_start_date': intervention.start,
                          'pd_ssfa_creation_date': intervention.created,
                          'pd_ssfa_end_date': intervention.end,

                          'cash_contribution': intervention.total_unicef_cash or 0,
                          'supply_contribution': intervention.total_in_kind_amount or 0,
                          'total_budget': intervention.total_budget or 0,
                          'unicef_budget': intervention.total_unicef_budget or 0,

                          'currency': intervention.planned_budget.currency if planned_budget else '-',
                          'partner_contribution': intervention.planned_budget.partner_contribution if planned_budget else '-',
                          'unicef_cash': intervention.planned_budget.unicef_cash if planned_budget else '-',
                          'in_kind_amount': intervention.planned_budget.in_kind_amount if planned_budget else '-',
                          'total': intervention.planned_budget.total if planned_budget else '-',
                          'fr_numbers_against_pd_ssfa': ' - '.join([fh.fr_number for fh in intervention.frs.all()]),
                          'fr_currencies': ', '.join(fr for fr in fr_currencies),
                          'sum_of_all_fr_planned_amount': intervention.frs.aggregate(
                              total=Coalesce(Sum('intervention_amt'), 0))[
                              'total'] if fr_currencies.count() <= 1 else '-',
                          'core_value_attached': has_assessment,
                          'partner_link': '{}/pmp/partners/{}/details'.format(base_url, partner.pk),
                          'intervention_link': '{}/pmp/interventions/{}/details'.format(base_url, intervention.pk),
                          }
                op = process(PMPIndicators, filters=dict(country_name=country.name,
                                                         schema_name=country.schema_name,
                                                         country_id=partner.id,
                                                         partner_id=partner.pk,
                                                         intervention_id=intervention.pk),
                             values=values)
                results.incr(op)
                # existing, created = PMPIndicators.objects.get_or_create(country_name=country.name,
                #                                                         schema_name=country.schema_name,
                #                                                         country_id=partner.id,
                #                                                         partner_id=partner.pk,
                #                                                         intervention_id=intervention.pk,
                #                                                         defaults=values)
                # if created:
                #     results.created += 1
                # else:
                #     if is_record_changed(existing, values):
                #         results.updated += 1
                #         PMPIndicators.objects.update_or_create(country_name=country.name,
                #                                                schema_name=country.schema_name,
                #                                                country_id=partner.id,
                #                                                partner_id=partner.pk,
                #                                                intervention_id=intervention.pk,
                #                                                defaults=values)
                #     else:
                #         results.unchanged += 1

    return results.as_dict()
    #             PMPIndicators.objects.create(
    #                 country_id=country.pk,
    #                 partner_id=partner.pk,
    #                 intervention_id=intervention.pk)
    #             created[country.name] += 1
    #
    # return created


@app.etl(Intervention)
def load_intervention():
    connection = connections['etools']
    countries = connection.get_tenants()
    results = EtlResult()
    for country in countries:
        connection.set_schemas([country.schema_name])
        qs = PartnersIntervention.objects.all().select_related('agreement',
                                                               'partner_authorized_officer_signatory',
                                                               'unicef_signatory',
                                                               'country_programme',
                                                               )
        num = 0
        for num, record in enumerate(qs, 1):
            values = dict(number=record.number,
                          title=record.title,
                          status=record.status,
                          start_date=record.start,
                          end_date=record.end,
                          review_date_prc=record.review_date_prc,
                          prc_review_document=record.prc_review_document,
                          partner_name=record.agreement.partner.name,
                          agreement_id=record.agreement.pk,
                          partner_authorized_officer_signatory_id=get_attr(record,
                                                                           'partner_authorized_officer_signatory.pk'),
                          country_programme_id=get_attr(record, 'country_programme.pk'),
                          intervention_id=record.pk,
                          unicef_signatory_id=get_attr(record, 'unicef_signatory.pk'),

                          signed_by_unicef_date=record.signed_by_unicef_date,
                          signed_by_partner_date=record.signed_by_partner_date,
                          population_focus=record.population_focus,
                          signed_pd_document=record.signed_pd_document,

                          submission_date=record.submission_date,
                          submission_date_prc=record.submission_date_prc,

                          unicef_signatory_first_name=get_attr(record,
                                                               'unicef_signatory.first_name'),
                          unicef_signatory_last_name=get_attr(record,
                                                              'unicef_signatory.last_name'),
                          unicef_signatory_email=get_attr(record, 'unicef_signatory.email'),

                          partner_signatory_title=get_attr(record,
                                                           'partner_authorized_officer_signatory.title'),
                          partner_signatory_first_name=get_attr(record,
                                                                'partner_authorized_officer_signatory.first_name'),
                          partner_signatory_last_name=get_attr(record,
                                                               'partner_authorized_officer_signatory.last_name'),
                          partner_signatory_email=get_attr(record,
                                                           'partner_authorized_officer_signatory.email'),
                          partner_signatory_phone=get_attr(record,
                                                           'partner_authorized_officer_signatory.phone'),

                          partner_focal_point_title=get_attr(record,
                                                             'partner_focal_point.title'),
                          partner_focal_point_first_name=get_attr(record,
                                                                  'partner_focal_point.first_name'),
                          partner_focal_point_last_name=get_attr(record,
                                                                 'partner_focal_point.last_name'),
                          partner_focal_point_email=get_attr(record,
                                                             'partner_focal_point.email'),
                          partner_focal_point_phone=get_attr(record,
                                                             'partner_focal_point.phone'),

                          metadata=record.metadata,
                          document_type=record.document_type,
                          updated=record.modified,
                          created=record.created,
                          )
            op = process(Intervention, filters=dict(country_name=country.name,
                                                    schema_name=country.schema_name,
                                                    intervention_id=record.pk),
                         values=values)
            results.incr(op)

            # existing, created = Intervention.objects.get_or_create(country_name=country.name,
            #                                                        schema_name=country.schema_name,
            #                                                        intervention_id=record.pk,
            #                                                        defaults=values)
            # if created:
            #     results.created += 1
            # else:
            #     if is_record_changed(existing, values):
            #         results.updated += 1
            #         Intervention.objects.update_or_create(country_name=country.name,
            #                                               schema_name=country.schema_name,
            #                                               intervention_id=record.pk,
            #                                               defaults=values)
            #     else:
            #         results.unchanged += 1

    return results.as_dict()


@app.etl(FAMIndicator)
def load_fam_indicator():
    connection = connections['etools']
    countries = connection.get_tenants()

    engagements = (AuditSpotcheck, AuditAudit, AuditSpecialaudit, AuditMicroassessment)
    start_date = date.today()  # + relativedelta(months=-1)
    results = EtlResult()
    for country in countries:
        connection.set_schemas([country.schema_name])
        for model in engagements:
            # indicator, created = FAMIndicator.objects.get_or_create(month=start_date,
            #                                                         country_name=country.name,
            #                                                         schema_name=country.schema_name)
            # if created:
            #     results.created += 1
            # changed = created
            realname = "_".join(model._meta.db_table.split('_')[1:])
            values = {}
            for status, status_display in AuditEngagement.STATUSES:
                filter_dict = {
                    'engagement_ptr__status': status,
                    'engagement_ptr__start_date__month': start_date.month,
                    'engagement_ptr__start_date__year': start_date.year,
                }
                field_name = f"{realname}_{status_display}".replace(" ", "_").lower()
                value = model.objects.filter(**filter_dict).count()
                values[field_name] = value
                # try:
                #     field_name = f"{realname}_{status_display}".replace(" ", "_").lower()
                #     value = model.objects.filter(**filter_dict).count()
                #     # just a safety check
                #     if not hasattr(indicator, field_name):  # pragma: no cover
                #         raise ValueError(field_name)
                #     if getattr(indicator, field_name) == value:
                #         changed = False
                #     else:
                #         changed = changed and True
                #         setattr(indicator, field_name, value)
                # except Exception as e:  # pragma: no cover
                #     logger.error(e)
                #     raise
            op = process(FAMIndicator, filters=dict(month=start_date,
                                                    country_name=country.name,
                                                    schema_name=country.schema_name),
                         values=values)
            results.incr(op)
    return results.as_dict()


@app.etl(UserStats)
def load_user_report():
    connection = connections['etools']
    countries = connection.get_tenants()
    today = date.today()
    first_of_month = datetime(today.year, today.month, 1)
    results = EtlResult()
    for country in countries:
        connection.set_schemas([country.schema_name])
        base = AuthUser.objects.filter(profile__country=country)
        values = {
            'total': base.count(),
            'unicef': base.filter(email__endswith='@unicef.org').count(),
            'logins': base.filter(
                last_login__month=first_of_month.month).count(),
            'unicef_logins': base.filter(
                last_login__month=first_of_month.month,
                email__endswith='@unicef.org').count(),
        }
        op = process(UserStats, filters=dict(month=first_of_month,
                                             country_name=country.name,
                                             schema_name=country.schema_name, ),
                     values=values)
        results.incr(op)

        # existing, created = UserStats.objects.get_or_create(month=first_of_month,
        #                                                     country_name=country.name,
        #                                                     schema_name=country.schema_name,
        #                                                     defaults=values)
        # if created:
        #     results.created += 1
        # else:
        #     if is_record_changed(existing, values):
        #         results.updated += 1
        #         UserStats.objects.update_or_create(month=first_of_month,
        #                                            country_name=country.name,
        #                                            schema_name=country.schema_name,
        #                                            defaults=values)
        #     else:
        #         results.unchanged += 1
    #
    return results.as_dict()
    # UserStats.objects.update_or_create(month=first_of_month,
    #                                    country_name=country.name,
    #                                    schema_name=country.schema_name,
    #                                    defaults=values)
    # created[country.name] += 1
    #
    # return created
