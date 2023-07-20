from django.db import models
from django.contrib.auth.models import AbstractUser  # , Permission
# from django.shortcuts import get_object_or_404


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, TimestampedModel):
    """A task manager user."""
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return self.get_full_name()

    # def user_gains_perms(request, user_id):
    #     user = get_object_or_404(User, pk=user_id)
    #     # any permission check will cache the current set of permissions
    #     user.has_perm('users.change_user')

    #     permission = Permission.objects.get(
    #         codename='change_user',
    #     )
    #     user.user_permissions.add(permission)

    #     # Checking the cached permission set
    #     user.has_perm('users.change_user')  # False

    #     # Request new instance of User
    #     # Be aware that user.refresh_from_db() won't clear the cache.
    #     user = get_object_or_404(User, pk=user_id)

    #     # Permission cache is repopulated from the database
    #     user.has_perm('users.change_user')  # True
