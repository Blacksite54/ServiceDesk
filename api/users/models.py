from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from api.core.user_manager import UserManager


class TypeUser(Enum):
    User = "1"
    Manager = "2"

class User(AbstractBaseUser):
    TYPE_USER = tuple((item.value, item.name) for item in TypeUser)

    email = models.EmailField(db_index=True, unique=True, null=True)
    type_user = models.CharField(max_length=2, choices=TYPE_USER, default=TypeUser.User.value)
    username = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = "email"
    objects = UserManager()
    model_objects = models.Manager()

    def __str__(self):
        return self.email
