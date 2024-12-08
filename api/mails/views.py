from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated

from api.core.utils import get_user_in_request
from api.mails.filters import TicketFilterBackend
from api.mails.models import Ticket, Message
from api.mails.serializers import TicketSerializer, TicketListSerializer, MessageSerializer


# TODO: можно разбить на 2: для пльзователей и для менеджеров и дописать permission_classes под менеджера
class TicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    filter_backends = (TicketFilterBackend,)

    def get_queryset(self):
        queryset = self.queryset.select_related(
        "user"
        )
        if self.action != "list":
            queryset = self.queryset.select_related(
                "manager",
            ).prefetch_related(
                "message",
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer

    def list(self, request, *args, **kwargs):
        user = get_user_in_request(request)

        tickets = self.filter_queryset(
            self.get_queryset().filter(
                Q(user__pk=user.pk) |
                Q(manager__pk=user.pk)
            )
        )

        page = self.paginate_queryset(tickets)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        try:
            ticket = self.get_queryset().filter(pk=pk).first()

        except Ticket.DoesNotExist:
            return Response(
                {"errors": {"detail": [_("Not found or permission denied.")]}},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ticket,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = get_user_in_request(request)

        try:
            ticket = self.get_queryset().filter(pk=user.pk).get()

        except Ticket.DoesNotExist:
            return Response(
                {"errors": {"detail": [_("Not found or permission denied.")]}},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer_data = request.data
        serializer = self.serializer_class(
            ticket,
            data=serializer_data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Message.objects.select_related(
        "ticket",
        "sender",
    )
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        user = get_user_in_request(request)
        ticket_id = request.data.get("ticket_id")

        messages = self.filter_queryset(
            self.get_queryset().filter(ticket=ticket_id, sender__pk=user.pk)
        )

        page = self.paginate_queryset(messages)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = get_user_in_request(request)

        serializer_context = {"sender": user}
        serializer_data = request.data

        serializer_class = self.get_serializer_class()

        serializer = serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        data_response = serializer.data
        return Response(data_response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = get_user_in_request(request)

        try:
            ticket = self.get_queryset().filter(pk=user.pk).get()

        except Ticket.DoesNotExist:
            return Response(
                {"errors": {"detail": [_("Not found or permission denied.")]}},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer_data = request.data
        serializer = self.serializer_class(
            ticket,
            data=serializer_data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)