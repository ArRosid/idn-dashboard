# Generated by Django 3.0.7 on 2020-06-11 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0017_auto_20200611_0948"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discount",
            name="kode",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
