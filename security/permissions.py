from rest_framework import permissions
from datetime import datetime
from .models import AccessPolicy

class ArgusAbacPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        user_dept = request.user.profile.department
        policy = AccessPolicy.objects.filter(target_department=user_dept).first()

        if policy:
            current_time = datetime.now().time()
            if not (policy.start_time <= current_time <= policy.end_time):
                return False

        return True

    def has_object_permission(self, request, view, obj):
        user_profile = request.user.profile

        is_owner = obj.owner == request.user
        is_in_dept = obj.department == user_profile.department

        if not (is_owner or is_in_dept):
            return False

        return user_profile.clearance_level >= obj.sensitivity_level