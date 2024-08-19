"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework.routers import DefaultRouter

from django_project.category_app.views import CategoryViewSet
from django_project.ticket_app.views import TicketViewSet
from django_project.user_app.views import UserViewSet

router = DefaultRouter()

router.register(r"api/categories", CategoryViewSet, basename="category")
router.register(r"api/tickets", TicketViewSet, basename="ticket")
router.register(r"api/users", UserViewSet, basename="user")

schema_view = get_schema_view(
    openapi.Info(
        title="Tickets API",
        default_version='v1',),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)