from django.db import models
from django.contrib.auth.models import User
from resources.models import Department
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    department = models.CharField(
        max_length=100, 
        choices=Department.choices,
        default=Department.ENGINEERING
    )

    clearance_level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.department})"



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class AccessPolicy(models.Model):
    name = models.CharField(max_length=100)
    target_department = models.CharField(
        max_length=100, 
        choices=Department.choices
    )
    required_clearance = models.IntegerField(default=1)


    start_time = models.TimeField(default="09:00:00")
    end_time = models.TimeField(default="17:00:00")

    def __str__(self):
        return f"Policy: {self.name} ({self.target_department})"