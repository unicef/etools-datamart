from django.contrib import admin

from unicef_security.admin import UserAdminPlus

from .models import User


@admin.register(User)
class UserAdminPlus(UserAdminPlus):
    pass
