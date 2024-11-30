from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    max_limit = 50

    def get_paginated_data(self, data) -> OrderedDict:
        return OrderedDict(
            [
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )
