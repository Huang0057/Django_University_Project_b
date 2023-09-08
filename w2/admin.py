from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password')


admin.site.register(UserProfile, UsersAdmin)