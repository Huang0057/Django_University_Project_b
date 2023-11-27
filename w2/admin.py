from django.contrib import admin
from .models import UserProfile, ArmMetrics, FootMetrics, LimbMetrics, HandMetrics, GameRecord,UserCheckIn
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(ArmMetrics)
admin.site.register(FootMetrics)
admin.site.register(LimbMetrics)
admin.site.register(HandMetrics)
admin.site.register(GameRecord)
admin.site.register(UserCheckIn)