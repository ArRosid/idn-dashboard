from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'created_at', 'updated_at']
    fieldsets = (
        (None, dict(fields=('email', 'password'))),
        (_('Personal Info'), {'fields': ('name', )}),
        (
            _("Permissions"),
            dict(fields=('is_active', 'is_staff', 'is_superuser'))
        ),
        (_('Important dates'), dict(fields=('last_login',)))
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
