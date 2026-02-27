from celery import shared_task
from .models import SecurityLog

@shared_task
def log_security_event(user_id, action, resource, reason, ip_address=None):
    SecurityLog.objects.create(
        user_id=user_id,
        action=action,
        resource=resource,
        reason=reason,
        ip_address=ip_address
    )
    return f"Security event {action} recorded for user {user_id}"