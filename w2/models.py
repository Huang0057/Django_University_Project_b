from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_UID = models.CharField(
        max_length=30, primary_key=True, unique=True)
    Arm_UID = models.CharField(max_length=20, unique=True)
    Foot_UID = models.CharField(max_length=20, unique=True)
    Limb_UID = models.CharField(max_length=20, unique=True)
    Hand_UID = models.CharField(max_length=20, unique=True)
    TotalCoin = models.IntegerField(default=0)

@receiver(post_save, sender=UserProfile)
def create_related_records(sender, instance, created, **kwargs):
    if created:  # 確保只有在創建新的UserProfile時才執行以下動作
        # 為ArmMetrics建立一個新記錄
        print(instance.Arm_UID)
        def create_metrics():
            ArmMetrics.objects.create(USER_UID=instance.USER_UID, Arm_UID=instance.Arm_UID)
            FootMetrics.objects.create(USER_UID=instance.USER_UID, Foot_UID=instance.Foot_UID)
            LimbMetrics.objects.create(USER_UID=instance.USER_UID, Limb_UID=instance.Limb_UID)
            HandMetrics.objects.create(USER_UID=instance.USER_UID, Hand_UID=instance.Hand_UID)
        transaction.on_commit(create_metrics)


class MetricsBase(models.Model):
    USER_UID = models.CharField(max_length=20)
    LastStage = models.CharField(max_length=20,default='0')
    TotalPlayTime = models.FloatField(default=0)
    TotalPlayCount = models.IntegerField(default=0)
    PassCount = models.IntegerField(default=0)
    TotalGetCoin = models.IntegerField(default=0)
    LastRecordId = models.CharField(max_length=20,default='0')

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
    USER_UID = models.CharField(max_length=20)
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
