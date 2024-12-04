from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# from etools_datamart.apps.mart.data import EtoolsLoader
# from etools_datamart.apps.mart.data import EtoolsDataMartModel
# from etools_datamart.apps.mart.data import add_location_mapping, LocationMixin
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.sources.etools.enrichment.consts import (
    ActionPointConsts,
    AuditEngagementConsts,
    CategoryConsts,
    PartnersInterventionConst,
)
from etools_datamart.apps.sources.etools.models import (
    ActionPointsActionpoint,
    AuditAudit,
    AuditMicroassessment,
    AuditSpecialaudit,
    AuditSpotcheck,
    DjangoComments,
    DjangoContentType,
    FieldMonitoringPlanningMonitoringactivity,
    PseaAssessment,
    T2FTravelactivity,
    TpmTpmactivity,
)

from .intervention import Intervention

# reference_number(self):
# return '{}/{}/{}/APD'.format(
#     connection.tenant.country_short_code or '',
#     self.created.year,
#     self.id,
# )
ENGAGEMENTS = [AuditSpotcheck, AuditMicroassessment, AuditSpecialaudit, AuditAudit]
ENGAGEMENTS_NAMES = [c.__name__ for c in ENGAGEMENTS]

RELATED_MODULES = ENGAGEMENTS + [
    TpmTpmactivity,
    T2FTravelactivity,
    PseaAssessment,
    FieldMonitoringPlanningMonitoringactivity,
]

RELATED_MODULE_NAMES = [c.__name__ for c in RELATED_MODULES]
RELATED_MODULE_CHOICES = zip(RELATED_MODULE_NAMES, RELATED_MODULE_NAMES)

"""
-- Set country schema
SET search_path = public, ##COUNTRY##;

-- Count for paging;
SELECT COUNT(*) AS "__count" FROM "action_points_actionpoint"

-- ActionPoint 
SELECT '##COUNTRY##' AS __schema, 
       "action_points_actionpoint"."id", 
       "action_points_actionpoint"."created", 
       "action_points_actionpoint"."modified", 
       "action_points_actionpoint"."status", 
       "action_points_actionpoint"."description", 
       "action_points_actionpoint"."due_date", 
       "action_points_actionpoint"."date_of_completion", 
       
       "action_points_actionpoint"."assigned_by_id",
       "assigned_by_auth_user"."password", 
       "assigned_by_auth_user"."last_login", 
       "assigned_by_auth_user"."is_superuser", 
       "assigned_by_auth_user"."username", 
       "assigned_by_auth_user"."first_name", 
       "assigned_by_auth_user"."last_name", 
       "assigned_by_auth_user"."email", 
       "assigned_by_auth_user"."is_staff", 
       "assigned_by_auth_user"."is_active", 
       "assigned_by_auth_user"."date_joined", 
       "assigned_by_auth_user"."middle_name", 
       "assigned_by_auth_user"."created", 
       "assigned_by_auth_user"."modified", 
       "assigned_by_auth_user"."preferences"

       "action_points_actionpoint"."assigned_to_id", 
       "assigned_to_auth_user"."password", 
       "assigned_to_auth_user"."last_login", 
       "assigned_to_auth_user"."is_superuser", 
       "assigned_to_auth_user"."username", 
       "assigned_to_auth_user"."first_name", 
       "assigned_to_auth_user"."last_name", 
       "assigned_to_auth_user"."email", 
       "assigned_to_auth_user"."is_staff", 
       "assigned_to_auth_user"."is_active", 
       "assigned_to_auth_user"."date_joined", 
       "assigned_to_auth_user"."middle_name", 
       "assigned_to_auth_user"."created", 
       "assigned_to_auth_user"."modified", 
       "assigned_to_auth_user"."preferences"
       
       "action_points_actionpoint"."author_id", 
       "author_auth_user"."password", 
       "author_auth_user"."last_login", 
       "author_auth_user"."is_superuser", 
       "author_auth_user"."username", 
       "author_auth_user"."first_name", 
       "author_auth_user"."last_name", 
       "author_auth_user"."email", 
       "author_auth_user"."is_staff", 
       "author_auth_user"."is_active", 
       "author_auth_user"."date_joined", 
       "author_auth_user"."middle_name", 
       "author_auth_user"."created", 
       "author_auth_user"."modified", 
       "author_auth_user"."preferences"
              
       "action_points_actionpoint"."cp_output_id", 
       "reports_result"."name", 
       "reports_result"."code", 
       "reports_result"."result_type_id", 
       "reports_result"."sector_id", 
       "reports_result"."gic_code", 
       "reports_result"."gic_name", 
       "reports_result"."humanitarian_tag", 
       "reports_result"."level", 
       "reports_result"."lft", 
       "reports_result"."parent_id", 
       "reports_result"."rght", 
       "reports_result"."sic_code", 
       "reports_result"."sic_name", 
       "reports_result"."tree_id", 
       "reports_result"."vision_id", 
       "reports_result"."wbs", 
       "reports_result"."activity_focus_code", 
       "reports_result"."activity_focus_name", 
       "reports_result"."hidden", 
       "reports_result"."from_date", 
       "reports_result"."to_date", 
       "reports_result"."ram", 
       "reports_result"."country_programme_id", 
       "reports_result"."created", 
       "reports_result"."modified", 
       "reports_result"."humanitarian_marker_code", 
       "reports_result"."humanitarian_marker_name", 
       "reports_result"."programme_area_code", 
       "reports_result"."programme_area_name"

       "action_points_actionpoint"."engagement_id", 
       "action_points_actionpoint"."intervention_id", 
       "action_points_actionpoint"."location_id", 
       "action_points_actionpoint"."office_id", 

       "action_points_actionpoint"."partner_id", 
       "partners_partnerorganization"."id", 
       "partners_partnerorganization"."description", 
       "partners_partnerorganization"."address", 
       "partners_partnerorganization"."email", 
       "partners_partnerorganization"."phone_number", 
       "partners_partnerorganization"."alternate_id", 
       "partners_partnerorganization"."alternate_name", 
       "partners_partnerorganization"."rating", 
       "partners_partnerorganization"."core_values_assessment_date", 
       "partners_partnerorganization"."vision_synced", 
       "partners_partnerorganization"."type_of_assessment", 
       "partners_partnerorganization"."last_assessment_date", 
       "partners_partnerorganization"."hidden", 
       "partners_partnerorganization"."deleted_flag", 
       "partners_partnerorganization"."total_ct_cp", 
       "partners_partnerorganization"."total_ct_cy", 
       "partners_partnerorganization"."blocked", 
       "partners_partnerorganization"."city", 
       "partners_partnerorganization"."country", 
       "partners_partnerorganization"."postal_code", 
       "partners_partnerorganization"."shared_with", 
       "partners_partnerorganization"."street_address", 
       "partners_partnerorganization"."hact_values", 
       "partners_partnerorganization"."created", 
       "partners_partnerorganization"."modified", 
       "partners_partnerorganization"."net_ct_cy", 
       "partners_partnerorganization"."reported_cy", 
       "partners_partnerorganization"."total_ct_ytd", 
       "partners_partnerorganization"."basis_for_risk_rating", 
       "partners_partnerorganization"."manually_blocked", 
       "partners_partnerorganization"."outstanding_dct_amount_6_to_9_months_usd", 
       "partners_partnerorganization"."outstanding_dct_amount_more_than_9_months_usd", 
       "partners_partnerorganization"."highest_risk_rating_name", 
       "partners_partnerorganization"."highest_risk_rating_type", 
       "partners_partnerorganization"."psea_assessment_date", 
       "partners_partnerorganization"."sea_risk_rating_name", 
       "partners_partnerorganization"."lead_office_id", 
       "partners_partnerorganization"."lead_section_id", 

       "partners_partnerorganization"."organization_id"  
       "organizations_organization"."created", 
       "organizations_organization"."modified", 
       "organizations_organization"."name", 
       "organizations_organization"."vendor_number", 
       "organizations_organization"."organization_type", 
       "organizations_organization"."cso_type", 
       "organizations_organization"."short_name", 
       "organizations_organization"."other", 
       "organizations_organization"."parent_id"


       "action_points_actionpoint"."section_id", 

       "action_points_actionpoint"."tpm_activity_id", 
       
       "action_points_actionpoint"."high_priority", 
       
       "action_points_actionpoint"."travel_activity_id",
       "t2f_travelactivity"."travel_type",
       "t2f_travelactivity"."date", 
       "t2f_travelactivity"."partner_id", 
       "t2f_travelactivity"."partnership_id", 
       "t2f_travelactivity"."primary_traveler_id", 
       "t2f_travelactivity"."result_id",  

      
       "action_points_actionpoint"."category_id", 
       
       "action_points_actionpoint"."psea_assessment_id", 
       
       "action_points_actionpoint"."reference_number", 
       
       "action_points_actionpoint"."monitoring_activity_id" 

FROM "action_points_actionpoint"
     "assigned_by_auth_user"
     "assigned_to_auth_user" 
     "assigned_to_auth_user"
     "reports_result"
     "partners_partnerorganization"
     "organizations_organization" 
     "t2f_travelactivity"

ORDER BY "action_points_actionpoint"."id" ASC 
LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

-- 

-- 
SELECT "django_content_type"."id", 
       "django_content_type"."app_label", 
       "django_content_type"."model" 
FROM "django_content_type" 
WHERE ("django_content_type"."app_label" = 'action_points' 
        AND "django_content_type"."model" = 'actionpoint') 

SELECT '##COUNTRY##' AS __schema, 
       "django_comments"."id", 
       "django_comments"."object_pk", 
       "django_comments"."user_name", 
       "django_comments"."user_email", 
       "django_comments"."user_url", 
       "django_comments"."comment", 
       "django_comments"."submit_date", 
       "django_comments"."ip_address", 
       "django_comments"."is_public", 
       "django_comments"."is_removed", 
       "django_comments"."content_type_id", 
       "django_comments"."site_id", 
       "django_comments"."user_id" 
FROM "django_comments" 
WHERE ("django_comments"."content_type_id" = 270 
AND "django_comments"."object_pk" = '2')

"""


class ActionPointLoader(EtoolsLoader):
    def get_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        country = self.context["country"]
        return "{}/{}/{}/APD".format(country.country_short_code or "", record.created.year, record.id)

    # def get_category_module(self, original: ActionPointsActionpoint, values: dict):
    #     if original.engagement:
    #         return original.engagement.engagement_type

    def get_actions_taken(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        ct = DjangoContentType.objects.get(app_label="action_points", model="actionpoint")
        comments = DjangoComments.objects.filter(object_pk=record.id, content_type=ct)
        return ";\n\n".join(
            [
                "{} ({}): {}".format(c.user if c.user else "-", c.submit_date.strftime("%d %b %Y"), c.comment)
                for c in comments.all()
            ]
        )

    # def get_module_task_activity_reference_number(self, original: ActionPointsActionpoint, values: dict):
    #     if original.tpm_activity:
    #         return original.tpm_activity.tpm_visit.reference_number
    #
    def get_related_module_id(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        module = values["related_module_class"]
        if module in ENGAGEMENTS_NAMES:
            return record.engagement.pk
        elif module == "TpmTpmactivity":
            return record.tpm_activity.tpm_visit_id
        elif module == "T2FTravelactivity":
            return getattr(record.travel_activity.travels.filter(traveler=record.assigned_to).last(), "pk", None)
        elif module == "PseaAssessment":
            return record.psea_assessment.pk
        elif module == "FieldMonitoringPlanningMonitoringactivity":
            return record.monitoring_activity.pk
        elif module is None:
            return None
        raise ValueError(values["related_module_class"])

    def get_related_module_class(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        if record.engagement:
            for target in ENGAGEMENTS:
                try:
                    target.objects.get(engagement_ptr=record.engagement_id)
                    return target.__name__
                except ObjectDoesNotExist:
                    pass
            return "Error"
        elif record.tpm_activity:
            return "TpmTpmactivity"
        elif record.travel_activity:
            return "T2FTravelactivity"
        elif record.psea_assessment:
            return "PseaAssessment"
        elif record.monitoring_activity:
            return "FieldMonitoringPlanningMonitoringactivity"
        return None

    def get_engagement_subclass(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        # targets = [AuditSpotcheck, AuditMicroassessment, AuditSpecialaudit, AuditAudit]
        if not record.engagement:
            return None
        for target in ENGAGEMENTS:
            try:
                target.objects.get(engagement_ptr=record.engagement_id)
                return target.__name__
            except ObjectDoesNotExist:
                pass
        raise ValueError("Cannot find subclass for ActionPoint #%s Engagement %s" % (record.id, record.engagement_id))

    def get_intervention_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        intervention = record.intervention
        if intervention:
            agreement_base_number = intervention.agreement.agreement_number.split("-")[0]
            if intervention.document_type != PartnersInterventionConst.SSFA:
                number = "{agreement}/{type}{year}{id}".format(
                    agreement=agreement_base_number,
                    type=intervention.document_type,
                    year=intervention.reference_number_year,
                    id=intervention.id,
                )
                return number
            return agreement_base_number

    def get_module_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        if record.engagement:
            eng_type = record.engagement.engagement_type
            engagement_code = "a" if eng_type == AuditEngagementConsts.TYPE_AUDIT else eng_type
            return "{}/{}/{}/{}/{}".format(
                self.context["country"].country_short_code or "",
                record.partner.organization.name[:5],
                engagement_code.upper(),
                record.created.year,
                record.id,
            )
        elif record.tpm_activity:
            return record.tpm_activity.tpm_visit.reference_number
        elif record.psea_assessment:
            return record.psea_assessment.reference_number
        elif record.monitoring_activity:
            return record.monitoring_activity.number
        elif record.travel_activity:
            ta = record.travel_activity
            travel = ta.travels.filter(traveler=ta.primary_traveler).first()
            if not travel:
                return
            return travel.reference_number

    def get_module_task_activity_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        obj = record.related_object
        if not obj:
            return "n/a"

        if record.tpm_activity:
            return obj.tpm_visit.reference_number


class ActionPoint(LocationMixin, EtoolsDataMartModel):
    reference_number = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    author_username = models.CharField(max_length=200, blank=True, null=True)
    assigned_by_name = models.CharField(max_length=200, blank=True, null=True)
    assigned_by_email = models.CharField(max_length=200, blank=True, null=True)
    assigned_to_name = models.CharField(max_length=200, blank=True, null=True)
    assigned_to_email = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ActionPointConsts.STATUSES, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateTimeField(blank=True, null=True)
    high_priority = models.BooleanField(blank=True, null=True, db_index=True)
    cp_output = models.TextField(blank=True, null=True)
    cp_output_id = models.IntegerField(blank=True, null=True)

    # Intervention
    intervention_source_id = models.IntegerField(blank=True, null=True)
    intervention_number = models.CharField(max_length=64, blank=True, null=True)
    intervention_title = models.CharField(max_length=256, blank=True, null=True)

    office = models.CharField(max_length=64, blank=True, null=True)

    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)

    engagement_source_id = models.IntegerField(blank=True, null=True)
    engagement_type = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    engagement_subclass = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    related_module_class = models.CharField(
        max_length=64, choices=RELATED_MODULE_CHOICES, blank=True, null=True, db_index=True
    )
    related_module_id = models.IntegerField(blank=True, null=True, db_index=True)
    section_source_id = models.IntegerField(blank=True, null=True)
    section_type = models.CharField(max_length=64, blank=True, null=True)

    # tpm_activity_source_id = models.IntegerField()
    # tpm_activity = models.CharField(max_length=64, null=True)
    tpm_activity_source_id = models.IntegerField(blank=True, null=True)

    travel_activity_source_id = models.IntegerField(blank=True, null=True)
    travel_activity_travel_type = models.CharField(max_length=64, blank=True, null=True)

    category_source_id = models.IntegerField(blank=True, null=True)
    category_module = models.CharField(max_length=64, choices=CategoryConsts.MODULE_CHOICES, blank=True, null=True)
    category_description = models.CharField(max_length=300, blank=True, null=True)

    actions_taken = models.TextField(blank=True, null=True)
    module_reference_number = models.CharField(max_length=300, blank=True, null=True)
    module_task_activity_reference_number = models.CharField(max_length=300, blank=True, null=True)
    # related_module_url = models.CharField(max_length=300, blank=True, null=True)
    # action_point_url = models.CharField(max_length=300, blank=True, null=True)

    loader = ActionPointLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = ActionPointsActionpoint
        depends = (Intervention,)
        mapping = add_location_mapping(
            dict(
                assigned_by_name="assigned_by.get_display_name",
                assigned_by_email="assigned_by.email",
                assigned_to_name="assigned_to.get_display_name",
                assigned_to_email="assigned_to.email",
                author_username="author.username",
                category_description="category.description",
                category_module="category.module",
                category_source_id="category.id",
                cp_output="cp_output.name",
                cp_output_id="cp_output.id",
                engagement_source_id="engagement.id",
                engagement_type="engagement.engagement_type",
                intervention_source_id="intervention.id",
                intervention_title="intervention.title",
                office="office.name",
                partner_name="partner.organization.name",
                partner_source_id="partner.id",
                section_source_id="section.id",
                section_type="section.name",
                tpm_activity_source_id="tpm_activity.id",
                travel_activity_source_id="travel_activity.id",
                travel_activity_travel_type="travel_activity.travel_type",
                vendor_number="partner.organization.vendor_number",
            )
        )
