from unicef_rest_framework.views import URFReadOnlyModelViewSet

from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.sources.unpp import models


class AgencyAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgencyAgency
        exclude = ()


class AgencyAgencyViewSet(URFReadOnlyModelViewSet):
    serializer_class = AgencyAgencySerializer
    queryset = models.AgencyAgency.objects.all()


class AgencyAgencymemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgencyAgencymember
        exclude = ()


class AgencyAgencymemberViewSet(URFReadOnlyModelViewSet):
    serializer_class = AgencyAgencymemberSerializer
    queryset = models.AgencyAgencymember.objects.all()


class AgencyAgencyofficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgencyAgencyoffice
        exclude = ()


class AgencyAgencyofficeViewSet(URFReadOnlyModelViewSet):
    serializer_class = AgencyAgencyofficeSerializer
    queryset = models.AgencyAgencyoffice.objects.all()


class AgencyAgencyprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgencyAgencyprofile
        exclude = ()


class AgencyAgencyprofileViewSet(URFReadOnlyModelViewSet):
    serializer_class = AgencyAgencyprofileSerializer
    queryset = models.AgencyAgencyprofile.objects.all()


class AgencyOtheragencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgencyOtheragency
        exclude = ()


class AgencyOtheragencyViewSet(URFReadOnlyModelViewSet):
    serializer_class = AgencyOtheragencySerializer
    queryset = models.AgencyOtheragency.objects.all()


class CommonAdminlevel1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonAdminlevel1
        exclude = ()


class CommonAdminlevel1ViewSet(URFReadOnlyModelViewSet):
    serializer_class = CommonAdminlevel1Serializer
    queryset = models.CommonAdminlevel1.objects.all()


class CommonCommonfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonCommonfile
        exclude = ()


class CommonCommonfileViewSet(URFReadOnlyModelViewSet):
    serializer_class = CommonCommonfileSerializer
    queryset = models.CommonCommonfile.objects.all()


class CommonPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonPoint
        exclude = ()


class CommonPointViewSet(URFReadOnlyModelViewSet):
    serializer_class = CommonPointSerializer
    queryset = models.CommonPoint.objects.all()


class CommonSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonSector
        exclude = ()


class CommonSectorViewSet(URFReadOnlyModelViewSet):
    serializer_class = CommonSectorSerializer
    queryset = models.CommonSector.objects.all()


class CommonSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonSpecialization
        exclude = ()


class CommonSpecializationViewSet(URFReadOnlyModelViewSet):
    serializer_class = CommonSpecializationSerializer
    queryset = models.CommonSpecialization.objects.all()


class ExternalsPartnervendornumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExternalsPartnervendornumber
        exclude = ()


class ExternalsPartnervendornumberViewSet(URFReadOnlyModelViewSet):
    serializer_class = ExternalsPartnervendornumberSerializer
    queryset = models.ExternalsPartnervendornumber.objects.all()


class ExternalsUnicefvendordataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExternalsUnicefvendordata
        exclude = ()


class ExternalsUnicefvendordataViewSet(URFReadOnlyModelViewSet):
    serializer_class = ExternalsUnicefvendordataSerializer
    queryset = models.ExternalsUnicefvendordata.objects.all()


class NotificationNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationNotification
        exclude = ()


class NotificationNotificationViewSet(URFReadOnlyModelViewSet):
    serializer_class = NotificationNotificationSerializer
    queryset = models.NotificationNotification.objects.all()


class NotificationNotifieduserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationNotifieduser
        exclude = ()


class NotificationNotifieduserViewSet(URFReadOnlyModelViewSet):
    serializer_class = NotificationNotifieduserSerializer
    queryset = models.NotificationNotifieduser.objects.all()


class PartnerPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartner
        exclude = ()


class PartnerPartnerViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerSerializer
    queryset = models.PartnerPartner.objects.all()


class PartnerPartnerLocationFieldOfficesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerLocationFieldOffices
        exclude = ()


class PartnerPartnerLocationFieldOfficesViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerLocationFieldOfficesSerializer
    queryset = models.PartnerPartnerLocationFieldOffices.objects.all()


class PartnerPartnerauditassessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerauditassessment
        exclude = ()


class PartnerPartnerauditassessmentViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerauditassessmentSerializer
    queryset = models.PartnerPartnerauditassessment.objects.all()


class PartnerPartnerauditreportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerauditreport
        exclude = ()


class PartnerPartnerauditreportViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerauditreportSerializer
    queryset = models.PartnerPartnerauditreport.objects.all()


class PartnerPartnerauthorisedofficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerauthorisedofficer
        exclude = ()


class PartnerPartnerauthorisedofficerViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerauthorisedofficerSerializer
    queryset = models.PartnerPartnerauthorisedofficer.objects.all()


class PartnerPartnerbudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerbudget
        exclude = ()


class PartnerPartnerbudgetViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerbudgetSerializer
    queryset = models.PartnerPartnerbudget.objects.all()


class PartnerPartnercapacityassessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnercapacityassessment
        exclude = ()


class PartnerPartnercapacityassessmentViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnercapacityassessmentSerializer
    queryset = models.PartnerPartnercapacityassessment.objects.all()


class PartnerPartnercollaborationevidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnercollaborationevidence
        exclude = ()


class PartnerPartnercollaborationevidenceViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnercollaborationevidenceSerializer
    queryset = models.PartnerPartnercollaborationevidence.objects.all()


class PartnerPartnercollaborationpartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnercollaborationpartnership
        exclude = ()


class PartnerPartnercollaborationpartnershipViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnercollaborationpartnershipSerializer
    queryset = models.PartnerPartnercollaborationpartnership.objects.all()


class PartnerPartnerdirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerdirector
        exclude = ()


class PartnerPartnerdirectorViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerdirectorSerializer
    queryset = models.PartnerPartnerdirector.objects.all()


class PartnerPartnerexperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerexperience
        exclude = ()


class PartnerPartnerexperienceViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerexperienceSerializer
    queryset = models.PartnerPartnerexperience.objects.all()


class PartnerPartnerfundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerfunding
        exclude = ()


class PartnerPartnerfundingViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerfundingSerializer
    queryset = models.PartnerPartnerfunding.objects.all()


class PartnerPartnergoverningdocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnergoverningdocument
        exclude = ()


class PartnerPartnergoverningdocumentViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnergoverningdocumentSerializer
    queryset = models.PartnerPartnergoverningdocument.objects.all()


class PartnerPartnerheadorganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerheadorganization
        exclude = ()


class PartnerPartnerheadorganizationViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerheadorganizationSerializer
    queryset = models.PartnerPartnerheadorganization.objects.all()


class PartnerPartnerinternalcontrolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerinternalcontrol
        exclude = ()


class PartnerPartnerinternalcontrolViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerinternalcontrolSerializer
    queryset = models.PartnerPartnerinternalcontrol.objects.all()


class PartnerPartnermailingaddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnermailingaddress
        exclude = ()


class PartnerPartnermailingaddressViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnermailingaddressSerializer
    queryset = models.PartnerPartnermailingaddress.objects.all()


class PartnerPartnermandatemissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnermandatemission
        exclude = ()


class PartnerPartnermandatemissionViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnermandatemissionSerializer
    queryset = models.PartnerPartnermandatemission.objects.all()


class PartnerPartnermemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnermember
        exclude = ()


class PartnerPartnermemberViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnermemberSerializer
    queryset = models.PartnerPartnermember.objects.all()


class PartnerPartnerotherinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerotherinfo
        exclude = ()


class PartnerPartnerotherinfoViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerotherinfoSerializer
    queryset = models.PartnerPartnerotherinfo.objects.all()


class PartnerPartnerpolicyareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerpolicyarea
        exclude = ()


class PartnerPartnerpolicyareaViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerpolicyareaSerializer
    queryset = models.PartnerPartnerpolicyarea.objects.all()


class PartnerPartnerprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerprofile
        exclude = ()


class PartnerPartnerprofileViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprofileSerializer
    queryset = models.PartnerPartnerprofile.objects.all()


class PartnerPartnerregistrationdocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerregistrationdocument
        exclude = ()


class PartnerPartnerregistrationdocumentViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerregistrationdocumentSerializer
    queryset = models.PartnerPartnerregistrationdocument.objects.all()


class PartnerPartnerreportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerreporting
        exclude = ()


class PartnerPartnerreportingViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerreportingSerializer
    queryset = models.PartnerPartnerreporting.objects.all()


class PartnerPartnerreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerreview
        exclude = ()


class PartnerPartnerreviewViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerreviewSerializer
    queryset = models.PartnerPartnerreview.objects.all()


class ProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectApplication
        exclude = ()


class ProjectApplicationViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectApplicationSerializer
    queryset = models.ProjectApplication.objects.all()


class ProjectApplicationLocationsProposalOfEoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectApplicationLocationsProposalOfEoi
        exclude = ()


class ProjectApplicationLocationsProposalOfEoiViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectApplicationLocationsProposalOfEoiSerializer
    queryset = models.ProjectApplicationLocationsProposalOfEoi.objects.all()


class ProjectApplicationfeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectApplicationfeedback
        exclude = ()


class ProjectApplicationfeedbackViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectApplicationfeedbackSerializer
    queryset = models.ProjectApplicationfeedback.objects.all()


class ProjectAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectAssessment
        exclude = ()


class ProjectAssessmentViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectAssessmentSerializer
    queryset = models.ProjectAssessment.objects.all()


class ProjectClarificationrequestanswerfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectClarificationrequestanswerfile
        exclude = ()


class ProjectClarificationrequestanswerfileViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectClarificationrequestanswerfileSerializer
    queryset = models.ProjectClarificationrequestanswerfile.objects.all()


class ProjectClarificationrequestquestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectClarificationrequestquestion
        exclude = ()


class ProjectClarificationrequestquestionViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectClarificationrequestquestionSerializer
    queryset = models.ProjectClarificationrequestquestion.objects.all()


class ProjectEoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoi
        exclude = ()


class ProjectEoiViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiSerializer
    queryset = models.ProjectEoi.objects.all()


class ProjectEoiFocalPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiFocalPoints
        exclude = ()


class ProjectEoiFocalPointsViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiFocalPointsSerializer
    queryset = models.ProjectEoiFocalPoints.objects.all()


class ProjectEoiInvitedPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiInvitedPartners
        exclude = ()


class ProjectEoiInvitedPartnersViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiInvitedPartnersSerializer
    queryset = models.ProjectEoiInvitedPartners.objects.all()


class ProjectEoiLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiLocations
        exclude = ()


class ProjectEoiLocationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiLocationsSerializer
    queryset = models.ProjectEoiLocations.objects.all()


class ProjectEoiReviewersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiReviewers
        exclude = ()


class ProjectEoiReviewersViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiReviewersSerializer
    queryset = models.ProjectEoiReviewers.objects.all()


class ProjectEoiSpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiSpecializations
        exclude = ()


class ProjectEoiSpecializationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiSpecializationsSerializer
    queryset = models.ProjectEoiSpecializations.objects.all()


class ProjectEoiattachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectEoiattachment
        exclude = ()


class ProjectEoiattachmentViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectEoiattachmentSerializer
    queryset = models.ProjectEoiattachment.objects.all()


class ProjectPinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectPin
        exclude = ()


class ProjectPinViewSet(URFReadOnlyModelViewSet):
    serializer_class = ProjectPinSerializer
    queryset = models.ProjectPin.objects.all()


class ReviewPartnerflagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewPartnerflag
        exclude = ()


class ReviewPartnerflagViewSet(URFReadOnlyModelViewSet):
    serializer_class = ReviewPartnerflagSerializer
    queryset = models.ReviewPartnerflag.objects.all()


class ReviewPartnerverificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewPartnerverification
        exclude = ()


class ReviewPartnerverificationViewSet(URFReadOnlyModelViewSet):
    serializer_class = ReviewPartnerverificationSerializer
    queryset = models.ReviewPartnerverification.objects.all()


class SanctionslistSanctioneditemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SanctionslistSanctioneditem
        exclude = ()


class SanctionslistSanctioneditemViewSet(URFReadOnlyModelViewSet):
    serializer_class = SanctionslistSanctioneditemSerializer
    queryset = models.SanctionslistSanctioneditem.objects.all()


class SanctionslistSanctionednameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SanctionslistSanctionedname
        exclude = ()


class SanctionslistSanctionednameViewSet(URFReadOnlyModelViewSet):
    serializer_class = SanctionslistSanctionednameSerializer
    queryset = models.SanctionslistSanctionedname.objects.all()


class SanctionslistSanctionednamematchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SanctionslistSanctionednamematch
        exclude = ()


class SanctionslistSanctionednamematchViewSet(URFReadOnlyModelViewSet):
    serializer_class = SanctionslistSanctionednamematchSerializer
    queryset = models.SanctionslistSanctionednamematch.objects.all()


class SequencesSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SequencesSequence
        exclude = ()


class SequencesSequenceViewSet(URFReadOnlyModelViewSet):
    serializer_class = SequencesSequenceSerializer
    queryset = models.SequencesSequence.objects.all()
