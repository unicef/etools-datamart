# -*- coding: utf-8 -*-
import logging
from datetime import date

from django.db import connections
from django.db.models import Sum
from django.db.models.functions import Coalesce
from strategy_field.utils import get_attr

from etools_datamart.apps.data.models import Intervention, PMPIndicators
from etools_datamart.apps.data.models.fam import FAMIndicator
from etools_datamart.apps.data.models.user import UserStats
from etools_datamart.apps.etools.models import (AuditAudit, AuditEngagement, AuditMicroassessment,
                                                AuditSpecialaudit, AuditSpotcheck, AuthUser, PartnersIntervention,
                                                PartnersPartnerorganization,)
from etools_datamart.celery import app

logger = logging.getLogger(__name__)


@app.etl(PMPIndicators)
def load_pmp_indicator():
    connection = connections['etools']
    countries = connection.get_tenants()
    PMPIndicators.objects.truncate()
    base_url = 'https://etools.unicef.org'
    created = {}

    for country in countries:
        created[country.name] = 0
        connection.set_schemas([country.schema_name])

        logger.info(u'Running on %s' % country.name)
        for partner in PartnersPartnerorganization.objects.all():
            # .prefetch_related(
            # 'partnerspartnerorganization_partners_corevaluesassessment_partner_id'):
            # .select_related('partnersintervention_partners_interventionbudget_intervention_id')
            for intervention in PartnersIntervention.objects.filter(agreement__partner=partner):
                planned_budget = getattr(intervention,
                                         'partnersintervention_partners_interventionbudget_intervention_id', None)
                fr_currencies = intervention.frs.all().values_list('currency', flat=True).distinct()
                has_assessment = bool(getattr(partner.current_core_value_assessment, 'assessment', False))
                PMPIndicators.objects.create(
                    country_id=country.pk,
                    partner_id=partner.pk,
                    intervention_id=intervention.pk,
                    **{
                        'country_name': country.name,
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
                            total=Coalesce(Sum('intervention_amt'), 0))['total'] if fr_currencies.count() <= 1 else '-',
                        'core_value_attached': has_assessment,
                        'partner_link': '{}/pmp/partners/{}/details'.format(base_url, partner.pk),
                        'intervention_link': '{}/pmp/interventions/{}/details'.format(base_url, intervention.pk),
                    })
                created[country.name] += 1
    return created


@app.etl(Intervention)
def load_intervention():
    connection = connections['etools']
    countries = connection.get_tenants()
    Intervention.objects.truncate()
    created = {}
    for country in countries:
        connection.set_schemas([country.schema_name])
        qs = PartnersIntervention.objects.all().select_related('agreement',
                                                               'partner_authorized_officer_signatory',
                                                               'unicef_signatory',
                                                               'country_programme',
                                                               )
        num = 0
        for num, record in enumerate(qs, 1):
            Intervention.objects.create(country_name=country.name,
                                        schema_name=country.schema_name,
                                        number=record.number,
                                        title=record.title,
                                        status=record.status,
                                        start_date=record.start,
                                        end_date=record.end,
                                        review_date_prc=record.review_date_prc,
                                        prc_review_document=record.prc_review_document,

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
        created[country.name] = num

    return created


@app.etl(FAMIndicator)
def load_fam_indicator():
    connection = connections['etools']
    countries = connection.get_tenants()

    engagements = (AuditSpotcheck, AuditAudit, AuditSpecialaudit, AuditMicroassessment)
    start_date = date.today()  # + relativedelta(months=-1)
    created = {}
    for country in countries:
        created[country.name] = 0

        connection.set_schemas([country.schema_name])
        for model in engagements:
            indicator, __ = FAMIndicator.objects.get_or_create(month=start_date,
                                                               country_name=country.name,
                                                               schema_name=country.schema_name)

            realname = "_".join(model._meta.db_table.split('_')[1:])
            for status, status_display in AuditEngagement.STATUSES:
                filter_dict = {
                    'engagement_ptr__status': status,
                    'engagement_ptr__start_date__month': start_date.month,
                    'engagement_ptr__start_date__year': start_date.year,
                }
                try:
                    field_name = f"{realname}_{status_display}".replace(" ", "_").lower()
                    value = model.objects.filter(**filter_dict).count()
                    # just a safety check
                    if not hasattr(indicator, field_name):  # pragma: no cover
                        raise ValueError(field_name)
                    setattr(indicator, field_name, value)
                except Exception as e:  # pragma: no cover
                    logger.error(e)
                    raise
            indicator.save()
            created[country.name] += 1

    return created


@app.etl(UserStats)
def load_user_report():
    connection = connections['etools']
    countries = connection.get_tenants()
    start_date = date.today()  # + relativedelta(months=-1)
    created = {}
    for country in countries:
        created[country.name] = 0
        connection.set_schemas([country.schema_name])
        base = AuthUser.objects.filter(profile__country=country)
        UserStats.objects.update_or_create(month=start_date,
                                           country_name=country.name,
                                           schema_name=country.schema_name,
                                           defaults={
                                               'total': base.count(),
                                               'unicef': base.filter(email__endswith='@unicef.org').count(),
                                               'logins': base.filter(
                                                   last_login__month=start_date.month).count(),
                                               'unicef_logins': base.filter(
                                                   last_login__month=start_date.month,
                                                   email__endswith='@unicef.org').count(),
                                           })
        created[country.name] += 1

    return created

    # start_date = kwargs.get('start_date', None)
    # if start_date:
    #     start_date = datetime.strptime(start_date.pop(), '%Y-%m-%d')
    # else:
    #     start_date = date.today() + relativedelta(months=-1)
    #
    # countries = kwargs.get('countries', None)
    # qs = Country.objects.exclude(schema_name__in=['public', 'uat', 'frg'])
    # if countries:
    #     qs = qs.filter(schema_name__in=countries.pop().split(','))
    # fieldnames = ['Country', 'Total Users', 'Unicef Users', 'Last month Users', 'Last month Unicef Users']
    # dict_writer = writer(fieldnames=fieldnames)
    # dict_writer.writeheader()
    #
    # for country in qs:
    #     dict_writer.writerow({
    #         'Country': country,
    #         'Total Users': get_user_model().objects.filter(profile__country=country).count(),
    #         'Unicef Users': get_user_model().objects.filter(
    #             profile__country=country,
    #             email__endswith='@unicef.org'
    #         ).count(),
    #         'Last month Users': get_user_model().objects.filter(
    #             profile__country=country,
    #             last_login__gte=start_date
    #         ).count(),
    #         'Last month Unicef Users': get_user_model().objects.filter(
    #             profile__country=country,
    #             email__endswith='@unicef.org',
    #             last_login__gte=start_date
    #         ).count(),
    #     })
