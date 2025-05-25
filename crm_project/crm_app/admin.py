from django.contrib import admin
from .models import CustomUser, Lead
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'department']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Lead)
