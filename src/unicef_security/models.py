from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField

app_label = 'unicef_security'


def get_businessarea_model():
    try:
        name = getattr(settings, 'BUSINESSAREA_MODEL', 'unicef_security.BusinessArea')
        setattr(settings, 'BUSINESSAREA_MODEL', name)
        model = django_apps.get_model(name, require_ready=False)
        if not issubclass(model, AbstractBusinessArea):
            raise ImproperlyConfigured("BUSINESSAREA_MODEL must be a subclass of AbstractBusinessArea")
        return name
    except ValueError:
        raise ImproperlyConfigured("BUSINESSAREA_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "BUSINESSAREA_MODEL refers to model '%s' that has not been installed" % settings.BUSINESSAREA_MODEL
        )
    #
    # name = getattr(settings, 'BUSINESSAREA_MODEL', 'unicef_security.BusinessArea')
    #
    # model = apps.get_model(name.split('.'))
    # assert isinstance(model, AbstractBusinessArea)
    # return model


class TimeStampedModel:
    last_modify_date = models.DateTimeField(editable=False, blank=True, auto_now_add=True,
                                            auto_now=True)


class Region(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        app_label = 'unicef_security'

    def __str__(self):
        return f"{self.name}"


class AbstractBusinessArea(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    long_name = models.CharField(_('long name'), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = CountryField()

    class Meta:
        app_label = 'unicef_security'
        abstract = True
        verbose_name = _('Business Area')
        verbose_name_plural = _('Business Areas')

    def __str__(self):
        return f"{self.name}"


class BusinessArea(AbstractBusinessArea, TimeStampedModel):
    class Meta:
        app_label = 'unicef_security'
        swappable = 'BUSINESSAREA_MODEL'


class User(AbstractUser, TimeStampedModel):
    # business_area = models.ForeignKey(settings.BUSINESSAREA_MODEL,
    #                                   null=True, blank=True,
    #                                   on_delete=models.CASCADE)
    azure_id = models.UUIDField(blank=True, unique=True, null=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'unicef_security'

    @cached_property
    def label(self):
        if self.display_name:
            return self.display_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}:"
        elif self.first_name:
            return self.first_name
        else:
            return self.username

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.label
        super().save(*args, **kwargs)


class Role(models.Model, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        app_label = 'unicef_security'
