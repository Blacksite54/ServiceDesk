from rest_framework.permissions import AllowAny

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Test description",
    ),
    permission_classes=[AllowAny],
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "email/",
        include(
            ("api.mails.urls", "mails"),
            namespace="mails"
        ),
        name="mails"
    ),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', RedirectView.as_view(url='/email/ticket/', permanent=False)),
]
