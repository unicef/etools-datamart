from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AttachmentsAttachmentflat

from .partner import Partner


class AttachmentLoader(EtoolsLoader):
    def get_queryset(self):
        return self.config.source.objects.select_related(
            "attachment",
            "attachment__file_type",
            "attachment__content_type",
            "attachment__uploaded_by",
        )

    def get_linked_to(self, record: AttachmentsAttachmentflat, values: dict, **kwargs):
        return None


class Attachment(EtoolsDataMartModel):
    # from AttachmentsAttachmentflat
    agreement_reference_number = models.CharField(max_length=100, blank=True, null=True)
    created = models.CharField(max_length=50, blank=True, null=True)
    file_link = models.CharField(max_length=1024, blank=True, null=True)
    filename = models.CharField(max_length=1024, blank=True, null=True)
    object_link = models.CharField(max_length=200, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    partner_type = models.CharField(max_length=150, blank=True, null=True)
    pd_ssfa = models.IntegerField(blank=True, null=True)
    pd_ssfa_number = models.CharField(max_length=64, blank=True, null=True)
    source = models.CharField(max_length=150, blank=True, null=True)
    vendor_number = models.CharField(max_length=50, blank=True, null=True)

    # UnicefAttachmentsAttachment
    attachment_source_id = models.IntegerField(blank=True, null=True)
    file = models.CharField(max_length=1024, blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    file_type_id = models.IntegerField(blank=True, null=True)
    hyperlink = models.CharField(max_length=1000, blank=True, null=True)
    code = models.CharField(max_length=64, blank=True, null=True)
    uploaded_by = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=255, blank=True, null=True)

    loader = AttachmentLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        depends = (Partner,)
        source = AttachmentsAttachmentflat
        mapping = dict(
            file="attachment.file",
            attachment_source_id="attachment.pk",
            file_type="attachment.file_type.name",
            file_type_id="file_type.pk",
            content_type="attachment.content_type.model",
            hyperlink="attachment.hyperlink",
            object_id="attachment.object_id",
            code="attachment.code",
            uploaded_by="attachment.uploaded_by.username",
            # linked_to='-',
            # ct='-',
        )
