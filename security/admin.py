from django.contrib import admin
from .models import UserProfile, AccessPolicy

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'clearance_level')
    list_filter = ('department',)

@admin.register(AccessPolicy)
class AccessPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_department', 'start_time', 'end_time', 'required_clearance')
    list_filter = ('target_department',)