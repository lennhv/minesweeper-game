import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()
