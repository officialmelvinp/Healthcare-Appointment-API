from django.contrib import admin
from django.urls import path, include
from users import routers as users_api_router
from django.conf import settings

admin.site.site_header = "hospital_api by Melvin"

auth_api_url = [
    #path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # OAuth2 provider endpoints
    path('', include('rest_framework_social_oauth2.urls')),  # Token authentication
]

if settings.DEBUG:
    auth_api_url.append(path('verify/', include('rest_framework.urls')))  # Login and logout

api_url_patterns = [
    path('auth/', include(auth_api_url)),
    path('accounts/', include(users_api_router.router.urls)),  # API account creation
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns)),  # Domain name for our API
]




# from django.contrib import admin
# from django.urls import path, include
# from users import routers as users_api_router
# from django.conf import settings

# admin.site.site_header = "hospital_api by Melvin"

# #auth_api_url =[] #2a

# auth_api_url = [
#     path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),# OAuth2 provider endpoints
#     path('social/', include('rest_framework_social_oauth2.urls')),# Token authentication
# ]


# if settings.DEBUG:#2b
#     auth_api_url.append(path('verify/', include('rest_framework.urls')))  # Login and logout


# api_url_patterns = [ #api url end points (1a)
#     path('auth/', include(auth_api_url)),#2c  # API authentication for our login log out to work
#     path('accounts/', include(users_api_router.router.urls)),  # API account creation
    
# ]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(api_url_patterns)), #1b Domain name for our api
# ]
