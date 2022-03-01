from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_active')
    ordering = ('username',)