# Generated by Django 3.0.7 on 2020-08-04 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0029_auto_20200709_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='diskon_pelajar',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discount',
            name='persen',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]