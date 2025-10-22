from rest_framework import serializers
from .models import Assignment, AssignmentSubmission

class AssignmentSerializer(serializers.ModelSerializer):
    lecture_title = serializers.CharField(source='lecture.title', read_only=True)
    teacher_name = serializers.CharField(source='created_by.user.name', read_only=True)
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'assignment_title', 'student',
            'student_name', 'file_url', 'submitted_at', 'grade']
        read_only_fields = ['submitted_at', 'grade', 'student']

