from django.db import models
from apps.lectures.models import Lecture
from apps.users.models import User

class Assignment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField() 
    due_date = models.DateField()
    file_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, null=True, blank=True)


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, null=True, blank=True)
    file_url = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(blank=True, null=True)
    teacher_feedback = models.TextField(blank=True, null=True)
