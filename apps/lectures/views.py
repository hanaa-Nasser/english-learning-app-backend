from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lecture
from .serializers import LectureSerializer

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only for teachers
        return hasattr(request.user, 'lecture_teacher')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.teacher.user == request.user

class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'lecture_teacher'):
            raise PermissionDenied("User is not registered as a teacher.")

        serializer.save(teacher=user.lecture_teacher)

    def perform_update(self, serializer):
       user = self.request.user
       lecture = self.get_object()
       if user.role != 'teacher' or lecture.teacher.user != user:
        raise PermissionDenied("You are not allowed to update this lecture.")
       serializer.save()

    def perform_destroy(self, instance):
       user = self.request.user
       if user.role != 'teacher' or instance.teacher.user != user:
        raise PermissionDenied("You are not allowed to delete this lecture.")
       instance.delete()
      
    def get_queryset(self):
       return Lecture.objects.all().order_by('-created_at')
     #   user = self.request.user
     #   if hasattr(user, 'lecture_teacher'):
      #      return Lecture.objects.filter(teacher=user.lecture_teacher).order_by('-created_at')
      #  elif hasattr(user, 'student'):
      #      return Lecture.objects.filter(students=user.student).order_by('-created_at')
      #  return Lecture.objects.none()

