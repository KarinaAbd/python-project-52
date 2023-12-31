from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (EntityProtectedMixin,
                                 HasPermissionUserChangeMixin,
                                 ProjectLoginRequiredMixin)
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.models import User


class UserListView(ListView):
    """List of all users."""
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[Any]:
        users = User.objects.exclude(username='admin')
        return users


class UserCreateView(SuccessMessageMixin, CreateView):
    """Create new user."""
    model = User
    form_class = UserForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'title': _('Create user'),
        'button_text': _('Register'),
    }


class UserUpdateView(ProjectLoginRequiredMixin,
                     HasPermissionUserChangeMixin,
                     SuccessMessageMixin,
                     UpdateView):
    """
    Update existing and logged in user.
    Only user can edit himself.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'layouts/form.html'
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully updated')
    denied_url = reverse_lazy('user_list')
    permission_denied_message = _('You have no rights to change another user.')


class UserDeleteView(ProjectLoginRequiredMixin,
                     HasPermissionUserChangeMixin,
                     EntityProtectedMixin,
                     SuccessMessageMixin,
                     DeleteView):
    """
    Delete existing and logged in user.
    The user can be deleted only if he isn't being used.
    """
    model = User
    template_name = 'layouts/delete.html'
    extra_context = {
        'title': _('Delete user'),
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully deleted')
    denied_url = reverse_lazy('user_list')
    permission_denied_message = _('You have no rights to change another user.')
    protected_message = _('Unable to delete a user because he is being used')

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = user.first_name + user.last_name
        return context
