from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

class Notification(models.Model):
    ROLE_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    ACTION_TYPES = [
        ('new_assignment', 'New Assignment'),
        ('new_lecture', 'New Lecture'),
        ('new_exam','New Exam'),
        ('assignment_graded', 'Assignment Graded')
    ]

    TARGET_TYPES = [
        ('assignment', 'Assignment'),
        ('lecture', 'Lecture'),
        ('exam', 'Exam'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications') 
    recipient_role = models.CharField(max_length=20, choices=ROLE_TYPES)   
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    target_type = models.CharField(max_length=50, choices=TARGET_TYPES)
    target_id = models.IntegerField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} → {self.title}"

