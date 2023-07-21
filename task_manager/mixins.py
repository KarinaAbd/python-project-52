from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class ProjectLoginRequiredMixin(LoginRequiredMixin):
    """
    Authentication check.
    Restricts access without authentication.
    """
    denied_url = reverse_lazy('login')
    denied_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.denied_message)
            return redirect(self.denied_url)
        return super().dispatch(request, *args, **kwargs)


class ProjectUserPassesTestMixin(UserPassesTestMixin):
    """
    Deny a request with a permission error
    if authentificated user try to change other one.
    """
    permission_denied_message = _('You have no rights to change another user.')

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.get_object() == self.request.user
