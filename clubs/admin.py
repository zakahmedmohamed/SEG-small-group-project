from django.contrib import admin

from clubs.models import Club, UserClubs
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username','first_name','last_name','email','is_active'
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


#admin.site.unregister()