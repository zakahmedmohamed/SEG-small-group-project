"""Congifuration of the adminstrative interface for clubs."""
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'chess_xp',
        'is_member', 'is_owner', 'is_officer'
    ]
