"""Nexus_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
schema_view = get_schema_view(
   openapi.Info(
      title="NEXUS_SERVICE API",
      default_version='v0.1',
    #   url='',
      description="Test API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.DjangoModelPermissions],
   authentication_classes=()
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dj-auth/', include('django.contrib.auth.urls')),

    path("password-reset/confirm/<uidb64>/<token>/",
       PasswordResetConfirmView.as_view(),
       name='password_reset_confirm'),
    path('auth/', include('authentication.urls')),
    path('auth/', include('dj_rest_auth.urls'), name='auth'),
    path('store/api/', include('store.urls')),
    path('core/api/', include('core.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('allauth.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')
]


if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
