from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=50)


class UserPlayHistoryTotal(models.Model):
    Username = models.CharField(max_length=50, null=False)
    Part = models.CharField(max_length=20)
    Stage = models.CharField(max_length=20)
    TotalPlaytimes = models.CharField(max_length=10)  # 以文字形式存儲，例如 "2:30"
    TotalGamePlay = models.IntegerField()
    TotalPasses = models.IntegerField()
    TotalCoinObtained = models.CharField(max_length=10)


class UserPlayHistory(models.Model):
    Username = models.CharField(max_length=50, null=False)
    Part = models.CharField(max_length=20)
    Stage = models.CharField(max_length=20)
    StartTime = models.CharField(max_length=10)  # 以文字形式存儲，例如 "2:30"
    EndTime = models.CharField(max_length=10)  # 以文字形式存儲，例如 "2:30"
    PlayTime = models.CharField(max_length=10)  # 以文字形式存儲，例如 "2:30"
    NumberOfTimes = models.CharField(max_length=20)
    Coins = models.CharField(max_length=10)
