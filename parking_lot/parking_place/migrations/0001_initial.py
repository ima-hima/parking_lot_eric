# Generated by Django 3.2.19 on 2023-05-06 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StatusType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        choices=[
                            ("Empty", "Empty"),
                            ("Adjacent", "Adjacent"),
                            ("Full", "Full"),
                        ],
                        max_length=8,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        choices=[
                            ("Motorcycle", "Motorcycle"),
                            ("Car", "Car"),
                            ("Van", "Van"),
                        ],
                        max_length=10,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParkingPlace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="parking_place.statustype",
                    ),
                ),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="parking_place.vehicletype",
                    ),
                ),
            ],
        ),
    ]
