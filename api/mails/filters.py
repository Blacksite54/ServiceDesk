from api.core.filters import BaseFilterAPI


class TicketFilterBackend(BaseFilterAPI):
    filter_keys = {
        "start_date": "created_at__gte",
    }

    custom_filter = {
        "status": lambda queryset, value: queryset.filter(
            status__in=list(map(lambda v: v.strip(), value.split(",")))
        ),
    }