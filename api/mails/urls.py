from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.mails.views import TicketViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"ticket", TicketViewSet)


urlpatterns = [
    path(r"", include(router.urls)),
]
