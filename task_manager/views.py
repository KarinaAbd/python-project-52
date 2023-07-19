from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLogInView(LoginView, SuccessMessageMixin):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    # form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    success_message = _('You are logged in')
    extra_context = {
        'button_text': _('Enter')
    }


class UserLogOutView(LogoutView):
    pass
