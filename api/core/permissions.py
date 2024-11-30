from rest_framework import exceptions

from api.users.models import User


def get_user(pk: int) -> User:

    user = User.objects.filter(pk=pk).first()
    if user is None:
        raise exceptions.PermissionDenied(None, None)

    return user
