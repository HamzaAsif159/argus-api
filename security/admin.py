from django.contrib import admin
from .models import UserProfile, AccessPolicy, SecurityLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'clearance_level')
    list_filter = ('department',)

@admin.register(AccessPolicy)
class AccessPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_department', 'start_time', 'end_time', 'required_clearance')
    list_filter = ('target_department',)


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'resource', 'reason', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)