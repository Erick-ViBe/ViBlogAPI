from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="ViBlog API",
      default_version='v1',
      description="Api to manage a blog application, with management of 'comments', 'user' and 'likes'",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="erickvb12@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/user/',
        include("users.urls")
    ),

    path(
        'api/',
        include("blogs.urls")
    ),

   url(
       r'^docs(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0),
       name='schema-json'
   ),

   url(
       r'^docs/$',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'
   ),
]
