from django.db import models
from django.conf import settings

class Department(models.TextChoices):
    HR = 'HR', 'Human Resources'
    FINANCE = 'FINANCE', 'Finance'
    ENGINEERING = 'ENGINEERING', 'Engineering'
    MARKETING = 'MARKETING', 'Marketing'

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    department = models.CharField(
        max_length=100, 
        choices=Department.choices, 
        default=Department.ENGINEERING
    )
    
    sensitivity_level = models.IntegerField(default=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} | {self.department}"