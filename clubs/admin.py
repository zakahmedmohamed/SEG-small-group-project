"""Congifuration of the adminstrative interface for clubs."""
from django.contrib import admin
from clubs.models import Club, UserClubs
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'username', 'first_name', 'last_name'
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'name','description','location'
    ]

@admin.register(UserClubs)
class UserClubsAdmin(admin.ModelAdmin):
    list_display = [
        'user','club','is_owner','is_officer','is_member'
    ]