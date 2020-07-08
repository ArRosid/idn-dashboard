from django.contrib import admin
from marketing.models import Interaksi

# Register your models here.


@admin.register(Interaksi)
class InteraksiAdmin(admin.ModelAdmin):
    list_display = (
        "tim_marketing",
        "nama_client",
        "sumber",
        "no_hp",
        "email",
        "fb",
        "ig",
    )
