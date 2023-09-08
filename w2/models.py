from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=50)
