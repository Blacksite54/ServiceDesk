from enum import Enum, unique

from django.db import models

from api.core.models import TimestampedModel
from api.users.models import User


@unique
class ActionTicket(Enum):
    OPEN = "1"
    IN_WORK = "2"
    COMPLETED = "3"


class Ticket(TimestampedModel):
    STATUS_TICKET = tuple((item.value, item.name) for item in ActionTicket)

    user = models.ForeignKey(User, related_name="ticket", null=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey(User, related_name="assigned_tickets", null=True, on_delete=models.SET_NULL)
    recipient = models.EmailField()
    title = models.CharField(max_length=500)
    status = models.CharField(max_length=2, choices=STATUS_TICKET, default=ActionTicket.OPEN.value)


class Message(TimestampedModel):
    ticket = models.ForeignKey(Ticket, related_name="message", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="message", null=True, on_delete=models.SET_NULL)
    message = models.TextField()
