from django.db import models
from django.contrib.auth.models import AbstractUser


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, TimestampedModel):
    """A task manager user."""

    def __str__(self) -> str:
        return self.get_full_name()
