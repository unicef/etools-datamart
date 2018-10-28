from django.contrib.auth.models import Group
from django.forms import ChoiceField, Select


class GroupChoiceField(ChoiceField):

    def __init__(self, **kwargs):
        names = list(Group.objects.values_list('name', flat=True))
        choices = [[i, i] for i in names]
        super().__init__(choices=choices, **kwargs)


class GroupChoice(Select):
    pass
