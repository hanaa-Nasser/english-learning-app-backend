from django.db import models

# Create your models here.

class ActionLog(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    ACTION_TYPE_CHOICES = [
        ('create_lecture', 'Create Lecture'),
        ('create_assignment', 'Create Assignment'),
        ('submit_assignment', 'Submit Assignment'),
        ('grade_assignment', 'Grade Assignment'),
        ('post_announcement', 'Post Announcement'),
    ]
    TARGET_TYPE_CHOICES = [
        ('lecture', 'Lecture'),
        ('assignment', 'Assignment'),
        ('announcement', 'Announcement'),
    ]
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='action_logs', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    target_id = models.IntegerField()
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role.capitalize()} {self.user.name} - {self.action_type}"
