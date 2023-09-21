from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from .models import UserPlayHistoryTotal
from .models import UserPlayHistory
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password')


admin.site.register(UserProfile, UsersAdmin)
admin.site.register(UserPlayHistoryTotal)
admin.site.register(UserPlayHistory)
