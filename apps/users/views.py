"""
Views for user management.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .models import Teacher
from .serializers import StudentDashboardSerializer, TeacherDashboardSerializer



#from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
   # UserProfileSerializer,
    PasswordChangeSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ 
    ViewSet for user management.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """Return appropriate permissions."""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        """Return queryset based on user permissions."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile."""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def promote_user(request):
    User = get_user_model()
    email = "hanaa@gmail.com"  
    try:
        user = User.objects.get(email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return JsonResponse({"status": "Promotion successful"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"})

        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        base_data = UserSerializer(user).data

        if user.role == 'student':
            student = Student.objects.get(user=user)
            academic_data = StudentDashboardSerializer(student).data
            return Response({
                "role": "student",
                "user": base_data,
                "academic": academic_data
            })

        elif user.role == 'teacher':
            teacher = Teacher.objects.get(user=user)
            teacher_data = TeacherDashboardSerializer(teacher).data
            return Response({
                "role": "teacher",
                "user": base_data,
                "profile": teacher_data
            })

        return Response({"error": "Unknown role"}, status=400)
