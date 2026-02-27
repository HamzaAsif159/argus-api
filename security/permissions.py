from rest_framework import permissions
from datetime import datetime
from .models import AccessPolicy
from .tasks import log_security_event

class ArgusAbacPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        user_dept = request.user.profile.department
        policy = AccessPolicy.objects.filter(target_department=user_dept).first()

        if policy:
            current_time = datetime.now().time()
            if not (policy.start_time <= current_time <= policy.end_time):
                log_security_event.delay(
                    user_id=request.user.id,
                    action="TIME_LOCK_DENIAL",
                    resource=view.__class__.__name__,
                    reason=f"Attempted access at {current_time}. Policy allows {policy.start_time}-{policy.end_time}.",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                return False

        return True

    def has_object_permission(self, request, view, obj):
        user_profile = request.user.profile

        is_owner = obj.owner == request.user
        is_in_dept = obj.department == user_profile.department

        if not (is_owner or is_in_dept):
            log_security_event.delay(
                user_id=request.user.id,
                action="DEPARTMENT_MISMATCH",
                resource=f"{obj.__class__.__name__}: {obj.id}",
                reason="User attempted to access a resource outside their department or ownership.",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return False

        if not (user_profile.clearance_level >= obj.sensitivity_level):
            log_security_event.delay(
                user_id=request.user.id,
                action="INSUFFICIENT_CLEARANCE",
                resource=f"{obj.__class__.__name__}: {obj.id}",
                reason=f"User clearance ({user_profile.clearance_level}) lower than required ({obj.sensitivity_level}).",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return False

        return True