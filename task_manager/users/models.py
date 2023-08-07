from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """A task manager user."""
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Creation date'))

    def __str__(self) -> str:
        return self.get_full_name()
