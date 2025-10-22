# """
# URL configuration for English Learning App Backend.
# """

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from allauth.account.views import password_reset_from_key



urlpatterns = [
    # Admin interface
    path('', lambda request: JsonResponse({'message': 'API is running ✅'})),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints
    path('api/v1/', include('apps.lectures.urls')),
    path('api/v1/', include('apps.notifications.urls')),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.assignments.urls')),

   

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    path(
        'accounts/password/reset/confirm/<uidb64>/<key>/',
        password_reset_from_key,
        name='password_reset_confirm'
    ),
]

 # Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Authentication
    # path('api/auth/', include('rest_framework_simplejwt.urls')),
    