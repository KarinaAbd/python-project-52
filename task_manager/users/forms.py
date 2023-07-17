from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )
