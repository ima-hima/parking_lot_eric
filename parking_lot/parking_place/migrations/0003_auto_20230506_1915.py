# Generated by Django 3.2.19 on 2023-05-06 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parking_place", "0002_auto_20230506_1913"),
    ]

    operations = [
        migrations.RenameField(
            model_name="parkingplace",
            old_name="statusType",
            new_name="status",
        ),
        migrations.RenameField(
            model_name="parkingplace",
            old_name="vehicleType",
            new_name="vehicle_type",
        ),
    ]
