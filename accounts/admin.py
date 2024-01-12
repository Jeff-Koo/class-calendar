from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from django.db.models import Count, Q
from django.urls import reverse


@admin.register(get_user_model())
class UserAdmin(auth_admin.UserAdmin):
    list_display = [
        'username',
        'email',
    ]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser')},
        ),
    )
    ordering = ['-date_joined']
    search_fields = ['email', 'full_name', 'username']

