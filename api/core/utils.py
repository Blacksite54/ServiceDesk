from api.users.models import User

from rest_framework.exceptions import PermissionDenied


def get_user_in_request(request, raise_exception=True) -> User:
    user = getattr(request, "user", None)
    if not user and raise_exception:
        raise PermissionDenied(None, None)
    return user