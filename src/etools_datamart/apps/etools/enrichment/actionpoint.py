from django.utils.translation import gettext as _

class CategoryConsts:
    MODULE_CHOICES = (
        ('apd', _('Action Points')),
        ('t2f', _('Trip Management')),
        ('tpm', _('Third Party Monitoring')),
        ('audit', _('Financial Assurance')),
    )

class ActionPointConsts:
    MODULE_CHOICES = CategoryConsts.MODULE_CHOICES

    STATUS_OPEN = 'open'
    STATUS_COMPLETED = 'completed'

    STATUSES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_COMPLETED, _('Completed')),
    )

    STATUSES_DATES = {
        STATUS_OPEN: 'created',
        STATUS_COMPLETED: 'date_of_completion'
    }

    KEY_EVENTS = (
        ('status_update', _('Status Update')),
        ('reassign', _('Reassign')),
    )
