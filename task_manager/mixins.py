from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import RedirectURLMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeletionMixin


class ProjectRedirectURLMixin(RedirectURLMixin):
    next_page = None
    success_message = None
    info_message = None

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            if self.success_message:
                messages.success(self.request, self.success_message)
            elif self.info_message:
                messages.info(self.request, self.info_message)
            return resolve_url(self.next_page)


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
    if authentificated user try to change not his stuff.
    """
    denied_url = None
    permission_denied_message = None

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.denied_url)
        return super().dispatch(request, *args, **kwargs)


class HandleUserPassesTestMixin(ProjectUserPassesTestMixin):

    def test_func(self):
        return self.get_object() == self.request.user


class DeleteTaskPassesTestMixin(ProjectUserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user


class ProjectDeletionMixin(DeletionMixin):
    """
    Deny a deletion
    if an object is used by other objects.
    """
    denied_url = None
    protected_message = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.denied_url)
