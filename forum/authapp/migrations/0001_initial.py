# Generated by Django 4.2.2 on 2023-07-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserRequests",
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
                ("ip", models.CharField(max_length=30, verbose_name="ip")),
                (
                    "request_count",
                    models.IntegerField(default=0, verbose_name="request_count"),
                ),
                (
                    "request_time",
                    models.DateTimeField(null=True, verbose_name="request_time"),
                ),
                (
                    "is_banned",
                    models.BooleanField(default=False, verbose_name="is_banned"),
                ),
                ("ban_time", models.DateTimeField(null=True, verbose_name="ban_time")),
            ],
        ),
    ]