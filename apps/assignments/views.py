from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='has-submitted')
    def has_submitted(self, request, pk=None):
        user = request.user
        if not hasattr(user, 'student'):
            raise PermissionDenied("Only students can check submission status.")

        assignment = self.get_object()
        submitted = AssignmentSubmission.objects.filter(
            assignment=assignment,
            student=user.student
        ).exists()

        return Response({'has_submitted': submitted})


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return AssignmentSubmission.objects.filter(
                assignment__lecture__teacher__user=user
            )
        elif user.role == 'student':
            return AssignmentSubmission.objects.filter(student=user.student)
        return AssignmentSubmission.objects.none()

    def perform_create(self, serializer):
       user = self.request.user
       if not hasattr(user, 'student'):
           raise PermissionDenied("Only students can submit assignments.")

       assignment = serializer.validated_data['assignment']
       already_submitted = AssignmentSubmission.objects.filter(
       assignment=assignment,
       student=user.student
       ).exists()

       if already_submitted:
        raise PermissionDenied("You have already submitted this assignment.")

       serializer.save(student=user.student)

   
    def perform_update(self, serializer):
        user = self.request.user
        submission = self.get_object()
        if user.role == 'teacher' and submission.assignment.lecture.teacher.user == user:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to grade this submission.")
    
    @action(detail=True, methods=['get'], url_path='is-graded')
    def is_graded(self, request, pk=None):
        submission = self.get_object()
        graded = submission.grade is not None
        return Response({'is_graded': graded})
