from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserForm
from .models import User


class UserCreateView(SuccessMessageMixin, CreateView):
    """Create new user."""
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    success_url = ' '
    success_message = _('User is successfully registered')
