# Generated by Django 3.0.7 on 2020-07-09 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0028_pointhistory_user"),
    ]

    operations = [
        migrations.AlterModelOptions(name="training", options={"ordering": ["name"]},),
    ]
