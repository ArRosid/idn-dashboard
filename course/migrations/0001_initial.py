# Generated by Django 3.0.7 on 2020-06-08 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MonthYearScheddule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "month",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Januari"),
                            (2, "Februari"),
                            (3, "Maret"),
                            (4, "April"),
                            (5, "Mei"),
                            (6, "Juni"),
                            (7, "Juli"),
                            (8, "Agustus"),
                            (9, "September"),
                            (10, "Oktober"),
                            (11, "November"),
                            (12, "Desember"),
                        ]
                    ),
                ),
                ("year", models.PositiveSmallIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="TrainingCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Training",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("duration", models.PositiveSmallIntegerField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.TrainingCategory",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Scheddule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "training_type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Training Offline"),
                            (1, "Training Online"),
                            (2, "Bootcamp"),
                            (3, "Premium Webinar"),
                            (4, "Free Webinar"),
                        ]
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "month_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.MonthYearScheddule",
                    ),
                ),
                (
                    "training",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.Training",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Registration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "training_type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Training Offline"),
                            (1, "Training Online"),
                            (2, "Bootcamp"),
                            (3, "Premium Webinar"),
                            (4, "Free Webinar"),
                        ]
                    ),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Not Paid"), (1, "Wait for Confirm"), (2, "Paid")],
                        default=0,
                    ),
                ),
                ("is_retraining", models.BooleanField(default=False)),
                (
                    "month_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.MonthYearScheddule",
                    ),
                ),
                (
                    "scheddule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.Scheddule",
                    ),
                ),
                (
                    "training",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.Training",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("user", "training")},},
        ),
        migrations.CreateModel(
            name="PaymentConfirm",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.IntegerField()),
                ("proof_of_payment", models.FileField(upload_to="")),
                (
                    "registration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.Registration",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "Payment Confirm",},
        ),
    ]
