from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLogInView(LoginView):
    template_name = 'form.html'
    extra_context = {
        'title': _('Log In'),
        'button_text': _('Enter')
    }
    next_page = reverse_lazy('index')
    success_message = _('You are logged in')

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            messages.success(self.request, self.success_message)
            return resolve_url(self.next_page)


class UserLogOutView(LogoutView):
    next_page = reverse_lazy('index')
    info_message = _('You are logged out')

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            messages.info(self.request, self.info_message)
            return resolve_url(self.next_page)
