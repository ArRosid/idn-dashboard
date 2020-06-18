from django.contrib import admin
from home.models import HiIDN


@admin.register(HiIDN)
class HiIDNAdmin(admin.ModelAdmin):
    list_display = ("nama", "pertanyaan")
