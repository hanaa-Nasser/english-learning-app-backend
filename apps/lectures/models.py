from django.db import models
from django.conf import settings
from django.conf import settings
from apps.users.models import Student

    
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lecture_teacher')
    name = models.CharField(max_length=100, unique=True , default="Mr. S")
    bio = models.TextField(blank=True)
    office_hours = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username    
    
class Lecture(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = models.TextField(blank=True, null=True)
    pdf =models.TextField(blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True, related_name='lectures') 
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lectures')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title