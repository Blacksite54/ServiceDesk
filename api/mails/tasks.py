from typing import Any

from api.core.task_states import TaskStatus
from api.mails.models import Ticket, Message
from api.main.celery import app
from api.notify.models import NotifyUser


@app.task(bind=True, default_retry_delay=300, max_retries=1)
def send_email_start_task(
    task_obj: Any, ticket_id: int,
):
    try:
        ticket: Ticket = (
            Ticket.objects.select_related(
                "managers",
                "user",
                "message",
            )
            .filter(pk=ticket_id)
            .get()
        )

    except Ticket.DoesNotExist:
        task_obj.update_state(
            state=TaskStatus.ERROR.value, meta={"error": "Ticket not found"}
        )
        return

    NotifyUser.objects.create(user=ticket.user, message=f"Your request has been received")

    task_obj.update_state(state=TaskStatus.SUCCESS.value)


@app.task(bind=True, default_retry_delay=300, max_retries=1)
def send_email_closed_task(
    task_obj: Any, ticket_id: int,
):
    try:
        ticket: Ticket = (
            Ticket.objects.select_related(
                "managers",
                "user",
                "message",
            )
            .filter(pk=ticket_id)
            .get()
        )

    except Ticket.DoesNotExist:
        task_obj.update_state(
            state=TaskStatus.ERROR.value, meta={"error": "Ticket not found"}
        )
        return

    NotifyUser.objects.create(user=ticket.user, message=f"The task is closed")

    task_obj.update_state(state=TaskStatus.SUCCESS.value)


@app.task(bind=True, default_retry_delay=300, max_retries=1)
def api_email_message(
    task_obj: Any, message_id: int
):
    try:
        message: Message = Message.objects.filter(pk=message_id)
    except Message.DoesNotExist:
        task_obj.update_state(
            state=TaskStatus.ERROR.value, meta={"error": "message not found"}
        )
        return
    task_obj.update_state(state=TaskStatus.SUCCESS.value)
    #TODO Здесь подключаете свою api email и отправляете сообщения с параметрами из Message
    pass
