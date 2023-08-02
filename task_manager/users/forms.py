from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class UserForm(UserCreationForm):
    """Form for user creation."""
    first_name = CharField(max_length=150,
                           required=True,
                           label=_("First name"))
    last_name = CharField(max_length=150,
                          required=True,
                          label=_("Last name"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )


class UserUpdateForm(BaseUserCreationForm):
    """Form to update user."""
    first_name = CharField(max_length=150,
                           required=True,
                           label=_("First name"))
    last_name = CharField(max_length=150,
                          required=True,
                          label=_("Last name"))

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )
