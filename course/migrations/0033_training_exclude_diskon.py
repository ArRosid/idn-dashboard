# Generated by Django 3.0.7 on 2020-08-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0032_auto_20200804_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='exclude_diskon',
            field=models.BooleanField(default=False),
        ),
    ]
