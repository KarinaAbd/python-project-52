from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import RedirectURLMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeletionMixin, FormMixin


class ProjectRedirectURLMixin(RedirectURLMixin):
    next_page = None
    success_message = None
    info_message = None

    def get_default_redirect_url(self):
        """Return the default redirect URL with message."""
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
    Show message about necessarity to log in and redirect on login page.
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
    Deny a request with a permission error message
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
    """Only user can change information about him or delete his profile."""
    def test_func(self):
        return self.get_object() == self.request.user


class DeleteTaskPassesTestMixin(ProjectUserPassesTestMixin):
    """Only author can delete his task."""
    def test_func(self):
        return self.get_object().author == self.request.user


class ProtectUsedObjectsDeletionMixin(DeletionMixin):
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


class ProjectFormMixin(FormMixin):

    def get_context_data(self, **kwargs):
        """To display the name of the object to be deleted."""
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = object.name
        return context
