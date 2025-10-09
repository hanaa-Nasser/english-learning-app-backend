"""
URL patterns for user management.
"""
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, promote_user
from django.urls import path, include



router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls + [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path("promote-user/", promote_user),
  
]