from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, role='teacher', **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    name = models.CharField(max_length=255)
    profile_photo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscription_status = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    
    def __str__(self):
       return f"Student: {self.user.get_full_name()}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile_teacher')
    bio = models.TextField(blank=True, null=True)
    office_hours = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)


    
    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"
    
@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model()
    email = "hanaa@gmail.com"
    password = "1234"

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)