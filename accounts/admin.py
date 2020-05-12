from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from accounts.models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    ordering = ["id"]
    list_display = ["email", "name", "get_company", "created_at"]
    fieldsets = (
        (None, dict(fields=("email", "password"))),
        (_("Personal Info"), {"fields": ("name",)}),
        (_("Permissions"), dict(fields=("is_active", "is_staff", "is_superuser"))),
        (_("Important dates"), dict(fields=("last_login",))),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    def get_company(self, instance):
        return instance.profile.company

    get_company.short_description = "Company"
