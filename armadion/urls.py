from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from armadion import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Armadion API",
        default_version='v1',
        description="API for Armadion",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
                  # Admin panel
                  path('admin/', admin.site.urls),
                  # API
                  path('contact-form/', include('contactform.urls')),
                  path('', include('doors.urls')),
                  # Documentation
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      re_path(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'utils.views.error404'
handler500 = 'utils.views.error500'