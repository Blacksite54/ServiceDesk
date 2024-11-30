from django.db import models

from api.core.models import TimestampedModel
from api.users.models import User


class NotifyUser(TimestampedModel):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.CharField(max_length=250, null=True, blank=True)
    is_view = models.BooleanField(default=False)
