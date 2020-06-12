from django.contrib import admin
from course.models import (
    Training,
    Registration,
    PaymentConfirm,
    TrainingCategory,
    Scheddule,
    DayScheddule,
    MonthYearScheddule,
    Discount,
    JadwalFile,
)


@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "duration", "price")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "training", "training_type", "scheddule")


@admin.register(PaymentConfirm)
class PaymentConfirmAdmin(admin.ModelAdmin):
    list_display = ("registration", "amount", "created_at")


@admin.register(Scheddule)
class SchedduleAdmin(admin.ModelAdmin):
    list_display = ("training", "training_type", "month_year", "day")


@admin.register(DayScheddule)
class DaySchedduleAdmin(admin.ModelAdmin):
    pass


@admin.register(MonthYearScheddule)
class MonthYearSchedduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("persen", "kode", "end_date")


@admin.register(JadwalFile)
class JadwalFileAdmin(admin.ModelAdmin):
    pass
