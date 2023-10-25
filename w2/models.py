from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    USER_UID = models.CharField(
        max_length=30, primary_key=True, unique=True, default=0)
    Arm_UID = models.CharField(max_length=20, unique=True)
    Foot_UID = models.CharField(max_length=20, unique=True)
    Limb_UID = models.CharField(max_length=20, unique=True)
    Hand_UID = models.CharField(max_length=20, unique=True)
    TotalCoin = models.IntegerField(default=0)


class MetricsBase(models.Model):
    USER_UID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    LastStage = models.CharField(max_length=20)
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20)

    class Meta:
        abstract = True


class ArmMetrics(MetricsBase):
    Arm_UID = models.CharField(max_length=30, unique=True)


class FootMetrics(MetricsBase):
    Foot_UID = models.CharField(max_length=30, unique=True)


class LimbMetrics(MetricsBase):
    Limb_UID = models.CharField(max_length=30, unique=True)


class HandMetrics(MetricsBase):
    Hand_UID = models.CharField(max_length=30, unique=True)


class GameRecord(models.Model):
    USER_UID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    PlayDate = models.DateField()
    PlayPart = models.CharField(max_length=20)
    UID = models.CharField(max_length=30)
    PlayStage = models.CharField(max_length=20)
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    DurationTime = models.DurationField()
    AddCoin = models.IntegerField(default=0)
    ExerciseCount = models.IntegerField(default=0)
    EstablishTime = models.DateTimeField(auto_now_add=True)
