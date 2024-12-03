from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AttachmentsAttachmentflat

from .partner import Partner


class AttachmentLoader(EtoolsLoader):
    """
    Load Queries:

    -- Set country schema
    SET search_path = public, ##COUNTRY##;

    -- Count for paging;
    SELECT COUNT(*) AS "__count" FROM "attachments_attachmentflat"

    SELECT '##COUNTRY##' AS __schema,
           "attachments_attachmentflat"."id",
           "attachments_attachmentflat"."partner",
           "attachments_attachmentflat"."partner_type",
           "attachments_attachmentflat"."vendor_number",
           "attachments_attachmentflat"."pd_ssfa_number",
           "attachments_attachmentflat"."file_type",
           "attachments_attachmentflat"."file_link",
           "attachments_attachmentflat"."uploaded_by",
           "attachments_attachmentflat"."attachment_id",
           "attachments_attachmentflat"."filename",
           "attachments_attachmentflat"."agreement_reference_number",
           "attachments_attachmentflat"."object_link",
           "attachments_attachmentflat"."source",
           "attachments_attachmentflat"."pd_ssfa",
           "attachments_attachmentflat"."created",
           "attachments_attachmentflat"."ip_address",

           "unicef_attachments_attachment"."id",
           "unicef_attachments_attachment"."created",
           "unicef_attachments_attachment"."modified",
           "unicef_attachments_attachment"."file",
           "unicef_attachments_attachment"."hyperlink",
           "unicef_attachments_attachment"."object_id",
           "unicef_attachments_attachment"."code",
           "unicef_attachments_attachment"."content_type_id",
           "unicef_attachments_attachment"."file_type_id",
           "unicef_attachments_attachment"."uploaded_by_id",
           "unicef_attachments_attachment"."ip_address",

           "django_content_type"."id",
           "django_content_type"."app_label",
           "django_content_type"."model",

           "unicef_attachments_filetype"."id",
           "unicef_attachments_filetype"."order",
           "unicef_attachments_filetype"."name",
           "unicef_attachments_filetype"."label",
           "unicef_attachments_filetype"."code",
           "unicef_attachments_filetype"."group",

           "auth_user"."id", "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "auth_user"."middle_name",
           "auth_user"."created",
           "auth_user"."modified",
           "auth_user"."preferences"

    FROM "attachments_attachmentflat"
    INNER JOIN "unicef_attachments_attachment" ON ("attachments_attachmentflat"."attachment_id" = "unicef_attachments_attachment"."id")
    LEFT OUTER JOIN "django_content_type" ON ("unicef_attachments_attachment"."content_type_id" = "django_content_type"."id")
    LEFT OUTER JOIN "unicef_attachments_filetype" ON ("unicef_attachments_attachment"."file_type_id" = "unicef_attachments_filetype"."id")
    LEFT OUTER JOIN "auth_user" ON ("unicef_attachments_attachment"."uploaded_by_id" = "auth_user"."id")
    ORDER BY "attachments_attachmentflat"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##
    """

    def get_queryset(self):
        return self.config.source.objects.select_related(
            "attachment",
            "attachment__file_type",
            "attachment__content_type",
            "attachment__uploaded_by",
        )
        # TODO: Limit the projected fields


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
            attachment_source_id="attachment.id",
            file_type="attachment.file_type.name",
            # file_type_id="file_type.pk"
            file_type_id="attachment.file_type.id",
            content_type="attachment.content_type.model",
            hyperlink="attachment.hyperlink",
            object_id="attachment.object_id",
            code="attachment.code",
            uploaded_by="attachment.uploaded_by.username",
            # linked_to='-',
            # ct='-',
        )
