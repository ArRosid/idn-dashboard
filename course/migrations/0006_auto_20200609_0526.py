# Generated by Django 3.0.7 on 2020-06-08 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0005_auto_20200609_0505"),
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
            options={"verbose_name": "Mont Year Scheddule",},
        ),
        migrations.CreateModel(
            name="DayScheddule",
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
                ("day", models.CharField(max_length=100)),
                (
                    "month_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.MonthYearScheddule",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="scheddule",
            name="day",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="course.DayScheddule",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="registration",
            name="month_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course.MonthYearScheddule",
            ),
        ),
        migrations.AlterField(
            model_name="scheddule",
            name="month_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course.MonthYearScheddule",
            ),
        ),
        migrations.DeleteModel(name="MonthYearDayScheddule",),
    ]
