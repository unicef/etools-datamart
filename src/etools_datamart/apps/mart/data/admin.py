import logging
from time import time

from django.contrib import messages
from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_extra_buttons.decorators import button
from adminactions.actions import export_as_csv, export_as_xls, mass_update
from adminfilters.filters import AllValuesComboFilter
from adminfilters.mixin import AdminFiltersMixin
from adminfilters.value import ValueFilter
from humanize import naturaldelta

from unicef_rest_framework.models import Service

from etools_datamart.apps.core.admin_mixins import DisplayAllMixin
from etools_datamart.apps.multitenant.admin import SchemaFilter
from etools_datamart.config import settings
from etools_datamart.libs.truncate import TruncateTableMixin
from etools_datamart.sentry import process_exception

from . import models

logger = logging.getLogger(__name__)


class DatamartChangeList(ChangeList):
    pass


class DataModelAdmin(TruncateTableMixin, DisplayAllMixin, ModelAdmin):
    actions = [mass_update, export_as_csv, export_as_xls]

    # def get_list_display(self, request):
    #     ret = self.list_display
    #     if ret == ('pk',):
    #         return [f.name for f in self.model._meta.fields]
    #     return ret

    def get_list_filter(self, request):
        if SchemaFilter not in self.list_filter:
            self.list_filter = (SchemaFilter,) + self.list_filter

        if "last_modify_date" not in self.list_filter:
            self.list_filter = self.list_filter + ("last_modify_date",)
        return self.list_filter

    def get_changelist(self, request, **kwargs):
        return DatamartChangeList

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # def get_readonly_fields(self, request, obj=None):
    #     if not request.user.is_superuser or not settings.DEBUG:
    #         self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
    #     return self.readonly_fields
    #
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if request.method == 'POST' and not request.user.is_superuser:
    #         redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
    #                                                            self.opts.model_name))
    #
    #         self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
    #         return HttpResponseRedirect(redirect_url)
    #     return self._changeform_view(request, object_id, form_url, extra_context)

    @button()
    def invalidate_cache(self, request):
        for s in Service.objects.all():
            if s.managed_model == self.model:
                s.invalidate_cache()

    @button()
    def api(self, request):
        for s in Service.objects.all():
            if s.managed_model == self.model:
                return HttpResponseRedirect(s.endpoint)
        return ""  # pragma: no cover

    @button()
    def service(self, request):
        for s in Service.objects.all():
            if s.managed_model == self.model:
                url = reverse("admin:%s_%s_change" % (Service._meta.app_label, Service._meta.model_name), args=[s.pk])
                return HttpResponseRedirect(url)
        return ""  # pragma: no cover

    @button()
    def queue(self, request):
        try:
            start = time()
            res = self.model.loader.task.delay()
            if settings.CELERY_TASK_ALWAYS_EAGER:  # pragma: no cover
                stop = time()
                duration = stop - start
                self.message_user(
                    request, "Data loaded in %s. %s" % (naturaldelta(duration), res.result), messages.SUCCESS
                )
            else:
                self.message_user(request, "ETL task scheduled", messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            process_exception(e)
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta, "changelist")))

    @button()
    def refresh(self, request):
        try:
            start = time()
            res = self.model.loader.task.apply()
            stop = time()
            duration = stop - start
            self.message_user(request, "Data loaded in %s. %s" % (naturaldelta(duration), res.result), messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            process_exception(e)
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta, "changelist")))


@register(models.PMPIndicators)
class PMPIndicatorsAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "partner_name", "partner_type", "area_code")
    list_filter = (
        ("partner_type", AllValuesComboFilter),
        ("pd_ssfa_status", AllValuesComboFilter),
    )
    search_fields = ("partner_name",)
    date_hierarchy = "pd_ssfa_creation_date"


@register(models.Intervention)
class InterventionAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "title", "document_type", "number", "status")
    list_filter = (
        SchemaFilter,
        ("document_type", AllValuesComboFilter),
        ("status", AllValuesComboFilter),
        "start_date",
    )
    search_fields = ("number", "title")
    date_hierarchy = "start_date"


@register(models.GeoName)
class GeoNameAdmin(ModelAdmin):
    list_display = (
        "lat",
        "lng",
        "name",
        "geoname_id",
    )
    search_fields = (
        "lat",
        "lng",
        "name",
    )


@register(models.InterventionByLocation)
class InterventionByLocationAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "title", "document_type", "location", "number", "status")
    list_filter = (
        SchemaFilter,
        ("document_type", AllValuesComboFilter),
        ("status", AllValuesComboFilter),
        "start_date",
    )
    search_fields = ("number", "title")
    date_hierarchy = "start_date"
    autocomplete_fields = ("location",)


@register(models.InterventionActivity)
class InterventionActivityAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "pd_number", "partner")
    list_filter = (SchemaFilter,)
    search_fields = ("pd_number", "partner")


@register(models.InterventionCountryProgramme)
class InterventionCountryProgrammeAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "pd_number", "partner")
    list_filter = (SchemaFilter,)
    search_fields = ("pd_number", "partner")


@register(models.InterventionEPD)
class InterventionEPDAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "pd_number", "partner")
    list_filter = (SchemaFilter,)
    search_fields = ("pd_number", "partner")


@register(models.InterventionManagementBudget)
class InterventionManagementBudgetAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "pd_number", "partner")
    list_filter = (SchemaFilter,)
    search_fields = ("pd_number", "partner")


@register(models.InterventionPlannedVisits)
class InterventionPlannedVisitsAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("partner_vendor_number", "partner_name", "pd_status", "pd_reference_number")
    list_filter = (SchemaFilter,)
    search_fields = ("partner_vendor_number", "partner_name", "pd_reference_number")


@register(models.InterventionReview)
class InterventionReviewAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ("country_name", "pd_number", "partner")
    list_filter = (SchemaFilter,)
    search_fields = ("pd_number", "partner")


@register(models.FAMIndicator)
class FAMIndicatorAdmin(DataModelAdmin):
    list_display = (
        "country_name",
        "schema_name",
        "month",
    )
    list_filter = (
        SchemaFilter,
        "month",
    )
    date_hierarchy = "month"


@register(models.UserStats)
class UserStatsAdmin(DataModelAdmin):
    list_display = ("country_name", "schema_name", "month", "total", "unicef", "logins", "unicef_logins")
    list_filter = (
        SchemaFilter,
        "month",
    )
    date_hierarchy = "month"


@register(models.HACT)
class HACTAdmin(DataModelAdmin):
    list_display = (
        "country_name",
        "schema_name",
        "year",
        "microassessments_total",
        "programmaticvisits_total",
        "followup_spotcheck",
        "completed_spotcheck",
        "completed_hact_audits",
        "completed_special_audits",
    )
    list_filter = (SchemaFilter, "year", "last_modify_date")


@register(models.Location)
class LocationAdmin(AdminFiltersMixin, DataModelAdmin):
    list_display = (
        "country_name",
        "schema_name",
        "name",
        "admin_level",
        "admin_level_name",
        "latitude",
        "longitude",
        "point",
    )
    # readonly_fields = ('parent', 'gateway')
    list_filter = ("level", ("parent__name", ValueFilter.factory(title="Parent", lookup_name="icontains")))
    search_fields = ("name",)
    autocomplete_fields = (
        "parent",
        "geoname",
    )
    actions = ["update_centroid", mass_update]
    mass_update_exclude = ["geom", "id"]
    mass_update_hints = []

    def update_centroid(self, request, queryset):
        queryset.update_centroid()

    @button()
    def batch_update_centroid(self, request):
        models.Location.objects.batch_update_centroid()


@register(models.Locationsite)
class LocationsiteAdmin(DataModelAdmin):
    list_display = ("name", "p_code", "is_active")


@register(models.FMOntrack)
class FMOntrackAdmin(DataModelAdmin):
    list_display = (
        "monitoring_activity",
        "entity",
        "entity_type",
        "narrative_finding",
        "overall_finding_rating",
        "status",
    )


@register(models.FMOptions)
class FMOptionsAdmin(DataModelAdmin):
    list_display = ("label", "question", "category", "is_custom", "is_active")
    list_filter = ("category", "is_custom", "is_active")


@register(models.FMQuestion)
class FMQuestionAdmin(DataModelAdmin):
    list_display = (
        "monitoring_activity",
        "title",
        "entity_instance",
        "entity_type",
        "answer_type",
        "collection_method",
        "answer",
        "summary_answer",
        "overall_finding",
    )


@register(models.FundsReservation)
class FundsReservationAdmin(DataModelAdmin):
    search_fields = ("fr_number", "pd_reference_number", "wbs")
    list_display = (
        "country_name",
        "fr_number",
        "pd_reference_number",
        "fr_type",
        "wbs",
        "overall_amount_dc",
        "actual_amt_local",
        "total_amt_local",
    )
    list_filter = ("fr_type",)
    date_hierarchy = "start_date"


@register(models.PDIndicator)
class PDIndicatorAdmin(DataModelAdmin):
    list_display = ("title", "unit", "display_type")
    # list_filter = ('disaggregatable', )


@register(models.Travel)
class TravelAdmin(DataModelAdmin):
    list_display = ("traveler_email", "supervisor_email", "created")
    date_hierarchy = "created"
    list_filter = (
        "international_travel",
        "office_name",
        "status",
        "completed_at",
        "approved_at",
        "end_date",
        "start_date",
    )
    search_fields = (
        "office_name",
        "traveler_email",
    )


@register(models.Partner)
class PartnerAdmin(DataModelAdmin):
    list_display = ("name", "partner_type", "vendor_number", "cso_type", "rating", "lead_office", "lead_section")
    date_hierarchy = "created"
    list_filter = ("partner_type", "last_pv_date", "hidden", "cso_type", "rating")
    search_fields = (
        "vendor_number",
        "name",
    )


@register(models.PartnerHact)
class PartnerHactAdmin(DataModelAdmin):
    list_display = ("name", "partner_type", "vendor_number", "cso_type", "rating")
    list_filter = ("partner_type", "cso_type", "rating")
    search_fields = (
        "vendor_number",
        "name",
    )


@register(models.PartnerStaffMember)
class PartnerStaffMemberAdmin(DataModelAdmin):
    list_display = (
        "title",
        "last_name",
        "first_name",
        "user",
        "email",
        "phone",
    )
    date_hierarchy = "created"
    list_filter = ("active",)


@register(models.TravelActivity)
class TravelActivityAdmin(DataModelAdmin):
    list_display = ("travel_reference_number", "date", "location_name", "partner_name", "primary_traveler")


@register(models.ActionPoint)
class ActionPointAdmin(DataModelAdmin):
    list_display = (
        "schema_name",
        "reference_number",
        # 'intervention_number',
        # 'engagement_type',
        # 'engagement_subclass',
        "category_module",
        "related_module_class",
        "related_module_id",
        "high_priority",
        "status",
    )
    list_filter = ("high_priority", "engagement_type", "status", "related_module_class", "category_module")
    search_fields = ("reference_number",)


@register(models.TPMVisit)
class TPMVisitAdmin(DataModelAdmin):
    list_display = ("start_date", "end_date", "partner_name")


@register(models.TPMActivity)
class TPMActivityAdmin(DataModelAdmin):
    list_display = ("date", "partner_name", "pd_ssfa_title", "schema_name")


@register(models.EtoolsUser)
class EtoolsUserAdmin(DataModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


@register(models.InterventionBudget)
class InterventionBudgetAdmin(DataModelAdmin):
    list_display = ("source_id", "schema_name", "reference_number", "agreement_reference_number")
    search_fields = ("reference_number", "agreement_reference_number")
    list_filter = ("status",)


@register(models.Office)
class OfficeAdmin(DataModelAdmin):
    list_display = ("name", "country_name", "area_code")


@register(models.Section)
class SectionAdmin(DataModelAdmin):
    list_display = (
        "name",
        "description",
        "alternate_name",
    )


@register(models.Agreement)
class AgreementAdmin(DataModelAdmin):
    list_display = (
        "agreement_type",
        "reference_number",
        "agreement_number",
        "partner_name",
    )
    list_filter = ("agreement_type", "status")


@register(models.Trip)
class TripAdmin(DataModelAdmin):
    list_display = (
        "reference_number",
        "traveler_name",
        "partner_name",
        "vendor_number",
        "end_date",
    )
    list_filter = ("start_date", "end_date")
    search_fields = ("reference_number",)


@register(models.TravelTrip)
class TravelTripAdmin(DataModelAdmin):
    list_display = (
        "reference_number",
        "traveler_email",
        "supervisor_email",
        "end_date",
    )
    list_filter = ("start_date", "end_date")
    search_fields = ("reference_number",)


@register(models.Engagement)
class EngagementAdmin(DataModelAdmin):
    list_display = ("reference_number", "agreement", "engagement_type", "status", "start_date", "sections")
    list_filter = ("engagement_type", "status", "start_date")
    search_fields = ("reference_number",)


@register(models.Grant)
class GrantAdmin(DataModelAdmin):
    list_display = ("name", "donor", "expiry")


@register(models.HACTHistory)
class HACTDetailAdmin(DataModelAdmin):
    list_display = ("schema_name", "year", "partner_name", "approach_threshold", "expiring_threshold", "sc_follow_up")
    list_filter = ("year", "approach_threshold", "expiring_threshold", "sc_follow_up")


@register(models.ReportIndicator)
class ReportIndicatorAdmin(DataModelAdmin):
    list_display = ("__str__",)
    list_filter = ()


@register(models.Attachment)
class AttachmentAdmin(DataModelAdmin):
    list_display = ("__str__",)
    list_filter = ("code", "content_type")
    search_fields = ("filename", "vendor_number", "agreement_reference_number", "pd_ssfa_number")


@register(models.AuditResult)
class AuditResultAdmin(DataModelAdmin):
    # list_display = ('vendor', 'partner_type', 'risk_rating')
    list_display = (
        "reference_number",
        "schema_name",
    )
    list_filter = ("reference_number", "source_id")


@register(models.SpotCheckFindings)
class SpotCheckAdmin(DataModelAdmin):
    list_display = ("reference_number", "schema_name", "status", "sections", "date_of_final_report")
    list_filter = ("engagement_type", "status")
    search_fields = ("reference_number", "source_id")


@register(models.MicroAssessment)
class MicroAssessmentAdmin(DataModelAdmin):
    list_display = ("reference_number", "engagement_type", "status")
    list_filter = ("engagement_type", "status")
    search_fields = ("reference_number", "source_id")


@register(models.Audit)
class AuditAdmin(DataModelAdmin):
    list_display = ("reference_number", "engagement_type", "status", "sections")
    list_filter = (
        "engagement_type",
        "status",
    )
    search_fields = ("reference_number", "source_id")


@register(models.AuditFinancialFinding)
class AuditFinancialFindingAdmin(DataModelAdmin):
    list_display = ("audit_reference_number", "audit_status", "partner_name")
    list_filter = (
        "partner_name",
        "audit_status",
    )
    search_fields = ("partner_name", "audit_reference_number", "source_id")


@register(models.AuditSpecial)
class AuditSpecialAdmin(DataModelAdmin):
    list_display = ("reference_number", "engagement_type", "status", "sections")
    list_filter = ("engagement_type", "status")
    search_fields = ("reference_number", "source_id")


@register(models.Result)
class ResultAdmin(DataModelAdmin):
    list_display = ("result_type", "name", "code", "country_programme", "wbs")
    list_filter = ("result_type", "country_programme")


@register(models.PseaAnswer)
class PseaAnswerAdmin(DataModelAdmin):
    list_display = (
        "assessment_partner_name",
        "assessment_vendor_number",
        "assessment_reference_number",
        "assessment_status",
        "assessment_date",
    )
    list_filter = ("assessment_status",)
    search_fields = ("assessment_partner_name", "assessment_vendor_number", "assessment_reference_number")


@register(models.PseaAssessment)
class PseaAssessmentAdmin(DataModelAdmin):
    list_display = ("partner_name", "vendor_number", "reference_number", "overall_rating", "status")
    list_filter = ("overall_rating", "status")
    search_fields = ("partner_name", "vendor_number", "reference_number")
