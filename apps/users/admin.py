from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Teacher

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ['email', 'name', 'role', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['email', 'name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['created_at']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model."""

    list_display = ['user', 'subscription_status', 'is_available']
    list_filter = ['subscription_status', 'is_available']
    search_fields = ['user__email', 'user__name']
    ordering = ['user__email']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin interface for Teacher model."""

    list_display = ['user', 'is_available', 'office_hours']
    list_filter = ['is_available']
    search_fields = ['user__email', 'user__name']
    ordering = ['user__email']
