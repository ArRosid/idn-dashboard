# Generated by Django 3.0.7 on 2020-06-11 01:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0015_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="discount",
            name="end_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
