from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USER_UID = models.CharField(max_length=20)
    Arm_UID = models.CharField(max_length=20)
    Foot_UID = models.CharField(max_length=20)
    Limb_UID = models.CharField(max_length=20)
    Hand_UID = models.CharField(max_length=20)
    TotalCoin = models.IntegerField(default=0)


class ArmMetrics(models.Model):
    Arm_UID = models.CharField(max_length=20)
    USER_UID = models.CharField(max_length=20)
    LastStage = models.CharField(max_length=20)
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20)


class FootMetrics(models.Model):
    Foot_UID = models.CharField(max_length=20)
    USER_UID = models.CharField(max_length=20)
    LastStage = models.CharField(max_length=20)
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20)


class LimbMetrics(models.Model):
    Limb_UID = models.CharField(max_length=20)
    USER_UID = models.CharField(max_length=20)
    LastStage = models.CharField(max_length=20)
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20)


class HandMetrics(models.Model):
    Hand_UID = models.CharField(max_length=20)
    USER_UID = models.CharField(max_length=20)
    LastStage = models.CharField(max_length=20)
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20)


class GameRecord(models.Model):
    USER_UID = models.CharField(max_length=20)
    PlayDate = models.DateField()
    PlayPart = models.CharField(max_length=20)
    UID = models.IntegerField()
    PlayStage = models.CharField(max_length=20)
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    DurationTime = models.DurationField()
    AddCoin = models.IntegerField(default=0)
    ExerciseCount = models.IntegerField(default=0)
    EstablishTime = models.DateTimeField(auto_now_add=True)
