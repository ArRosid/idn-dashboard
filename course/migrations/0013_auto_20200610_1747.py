# Generated by Django 3.0.7 on 2020-06-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0012_auto_20200610_0657"),
    ]

    operations = [
        migrations.AddField(
            model_name="training",
            name="price",
            field=models.CharField(default=2000000, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="paymentconfirm",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Not Paid"),
                    (1, "Wait for Confirm"),
                    (2, "Paid DP"),
                    (3, "Paid Lunas"),
                    (4, "Pembayaran di Tolak"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="registration",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Not Paid"),
                    (1, "Wait for Confirm"),
                    (2, "Paid DP"),
                    (3, "Paid Lunas"),
                    (4, "Pembayaran di Tolak"),
                ],
                default=0,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="training",
            unique_together={("category", "name", "duration", "price")},
        ),
    ]