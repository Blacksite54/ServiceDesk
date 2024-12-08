from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from api.core.serialize_fields.email import LowercaseEmailField
from api.mails.models import Ticket, Message, ActionTicket
from api.mails.tasks import send_email_start_task, send_email_closed_task, api_email_message
from api.users.models import User, TypeUser
from api.users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer[Message]):
    ticket_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Ticket.objects.all(),
        required=False,
        allow_null=True,
    )
    sender = UserSerializer(read_only=True)
    message = serializers.CharField()

    class Meta:
        model = Message
        fields = (
            "ticket",
            "ticket_id",
            "sender",
            "message",
        )

    def validate(self, attrs):
        if not attrs.get("message"):
            raise serializers.ValidationError(_('Field "message" is required.'))

        return attrs

    def create(self, validated_data):
        sender: User = self.context["sender"]
        ticket_id = validated_data.pop("ticket_id", None)

        validated_data["sender"] = sender

        if ticket_id:
            ticket = Ticket.objects.filter(pk=ticket_id).first()
            if ticket.status == ActionTicket.COMPLETED.value:
                raise serializers.ValidationError(_('Не пиши сюда больше))'))
        elif sender.type_user == TypeUser.User.value:
            ticket = Ticket.objects.create(
                user=sender,
            )
            send_email_start_task.delay(ticket.pk)
        else:
            raise serializers.ValidationError(_('the front sent the manager, so also without ticket_id.'))

        instance = Message.objects.create(**validated_data, ticket=ticket)
        api_email_message.delay()
        return instance


class TicketSerializer(serializers.ModelSerializer[Ticket]):
    user = UserSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, required=False, allow_null=True, allow_blank=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    recipient = LowercaseEmailField(required=False, allow_null=True, allow_blank=True)
    title = serializers.CharField(max_length=500, required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(max_length=2)

    class Meta:
        model = Ticket
        fields = (
            "user",
            "manager",
            "manager_id",
            "recipient",
            "title",
            "status",
        )

    def validate(self, attrs):
        manager_id = attrs.pop('manager_id', None)
        if manager_id:
            attrs["manager"] = manager_id
        return attrs

    def create(self, validated_data):

        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if instance.status == ActionTicket.COMPLETED.value:
            send_email_closed_task.delay(instance.pk)

        manager = validated_data.pop("manager", None)
        status = validated_data.pop("status", None)

        if manager and instance.manager is None:
            instance.manager = manager

        instance.status = status if status else instance.status
        instance.save()

        return instance



class TicketListSerializer(serializers.ModelSerializer[Ticket]):
    user = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=500, required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(max_length=2)

    class Meta:
        model = Ticket
        fields = (
            "user",
            "title",
            "status",
        )
