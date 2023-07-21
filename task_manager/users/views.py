from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (ProjectLoginRequiredMixin,
                                 ProjectUserPassesTestMixin)
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserListView(ListView):
    """List of all users."""
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[Any]:
        users = User.objects.exclude(username='admin')
        return users


class UserCreateView(SuccessMessageMixin, CreateView):
    """Create new user."""
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'title': _('Create user'),
        'button_text': _('Register'),
    }


class UserUpdateView(ProjectLoginRequiredMixin,
                     ProjectUserPassesTestMixin,
                     SuccessMessageMixin,
                     UpdateView):
    """
    Update existing and logged in user.
    The user can only edit himself.
    """
    model = User
    form_class = UserForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully updated')


class UserDeleteView(ProjectLoginRequiredMixin,
                     ProjectUserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    """
    Delete existing and logged in user.
    The user can only edit himself.
    """
    model = User
    template_name = 'delete.html'
    extra_context = {
        'title': _('Delete user'),
        # 'name': ,
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully deleted')
