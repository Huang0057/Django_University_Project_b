# Generated by Django 4.2.6 on 2023-11-01 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ArmMetrics",
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
                ("USER_UID", models.CharField(max_length=20)),
                ("LastStage", models.CharField(default="0", max_length=20)),
                ("TotalPlayTime", models.FloatField(default=0)),
                ("TotalPlayCount", models.IntegerField(default=0)),
                ("PassCount", models.IntegerField(default=0)),
                ("TotalGetCoin", models.IntegerField(default=0)),
                ("LastRecordId", models.CharField(default="0", max_length=20)),
                ("Arm_UID", models.CharField(max_length=30, unique=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="FootMetrics",
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
                ("USER_UID", models.CharField(max_length=20)),
                ("LastStage", models.CharField(default="0", max_length=20)),
                ("TotalPlayTime", models.FloatField(default=0)),
                ("TotalPlayCount", models.IntegerField(default=0)),
                ("PassCount", models.IntegerField(default=0)),
                ("TotalGetCoin", models.IntegerField(default=0)),
                ("LastRecordId", models.CharField(default="0", max_length=20)),
                ("Foot_UID", models.CharField(max_length=30, unique=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="GameRecord",
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
                ("USER_UID", models.CharField(max_length=20)),
                ("PlayDate", models.DateField()),
                ("PlayPart", models.CharField(max_length=20)),
                ("UID", models.CharField(max_length=30)),
                ("PlayStage", models.CharField(max_length=20)),
                ("StartTime", models.TimeField()),
                ("EndTime", models.TimeField()),
                ("DurationTime", models.DurationField()),
                ("AddCoin", models.IntegerField(default=0)),
                ("ExerciseCount", models.IntegerField(default=0)),
                ("EstablishTime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="HandMetrics",
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
                ("USER_UID", models.CharField(max_length=20)),
                ("LastStage", models.CharField(default="0", max_length=20)),
                ("TotalPlayTime", models.FloatField(default=0)),
                ("TotalPlayCount", models.IntegerField(default=0)),
                ("PassCount", models.IntegerField(default=0)),
                ("TotalGetCoin", models.IntegerField(default=0)),
                ("LastRecordId", models.CharField(default="0", max_length=20)),
                ("Hand_UID", models.CharField(max_length=30, unique=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="LimbMetrics",
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
                ("USER_UID", models.CharField(max_length=20)),
                ("LastStage", models.CharField(default="0", max_length=20)),
                ("TotalPlayTime", models.FloatField(default=0)),
                ("TotalPlayCount", models.IntegerField(default=0)),
                ("PassCount", models.IntegerField(default=0)),
                ("TotalGetCoin", models.IntegerField(default=0)),
                ("LastRecordId", models.CharField(default="0", max_length=20)),
                ("Limb_UID", models.CharField(max_length=30, unique=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "USER_UID",
                    models.CharField(
                        max_length=30, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("Arm_UID", models.CharField(max_length=20, unique=True)),
                ("Foot_UID", models.CharField(max_length=20, unique=True)),
                ("Limb_UID", models.CharField(max_length=20, unique=True)),
                ("Hand_UID", models.CharField(max_length=20, unique=True)),
                ("TotalCoin", models.IntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
