from django.contrib import admin
from django.urls import path, include
from users import routers as users_api_router
from Doctor import routers as doctor_api_router
from appointments import routers as appointment_api_router
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "hospital_api by Melvin"

# OAuth and authentication URLs
auth_api_url = [
    path('', include('rest_framework_social_oauth2.urls')),  # Token authentication
    
]

if settings.DEBUG:
    auth_api_url.append(path('verify/', include('rest_framework.urls')))  # Login and logout if DEBUG is True

# Main API URL patterns
api_url_patterns = [
    path('auth/', include(auth_api_url)),  # Authentication endpoints
    path('accounts/', include(users_api_router.router.urls)),  # User-related endpoints
    path('doctor/', include(doctor_api_router.router.urls)),  # Doctor-related endpoints
    path('appointment/', include(appointment_api_router.router.urls)),  # Appointment-related endpoints
]

# URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns)),  # Base API path
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
