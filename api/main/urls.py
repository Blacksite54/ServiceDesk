from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

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
    path('', RedirectView.as_view(url='/email/ticket/', permanent=False)),
]
