"""
Serializers for user models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Student
from .models import Teacher



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    

    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',  'name', 'email','phone_number', 'role',
             'profile_photo',
             'created_at','full_name'
            
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.name
class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'name', 'email','phone_number', 'password',
            'password_confirm'
            
        ]

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""

    class Meta:
        model = User
        fields = [
             'name',
            'profile_photo',
            'phone_number',
            'preferred_language',
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['status', 'total_marks', 'remaining_lectures']

class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['bio', 'office_hours', 'is_available']
