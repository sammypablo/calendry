# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'timezone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'timezone')}),
    )

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_time', 'end_time', 'event_type')
    list_filter = ('event_type', 'user')
    search_fields = ('title', 'description')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Event, EventAdmin)