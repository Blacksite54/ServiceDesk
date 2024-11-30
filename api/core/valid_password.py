from typing import Union

from api.users.models import User


class ValidUserPasswordMixin:
    def get_valid_password(
        self, password: str, email: str = None
    ) -> Union[User, None]:
        user: User = None

        user_query_set = User.model_objects.all()

        if not user and email:
            try:
                user = user_query_set.get(email=email)

            except User.DoesNotExist:
                user = None

        if not user or not user.check_password(password):
            return None

        return user
