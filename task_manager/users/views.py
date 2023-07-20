from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserForm
from .models import User


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
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'title': _('Create user'),
        'button_text': _('Create'),
    }


class UserUpdateView(UpdateView, SuccessMessageMixin, UserPassesTestMixin):
    """Update existing and logged in user.
    The user can only edit himself."""
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully updated')
    denied_url = reverse_lazy('login')
    denied_message = _('You are not logged in! Please log in.')
    permission_denied_message = _('You have no rights to change another user.')

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not request.user.is_authenticated:
            messages.error(self.request, self.denied_message)
            return redirect(self.denied_url)
        elif not user_test_result:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.get_object() == self.request.user


class UserDeleteView(SuccessMessageMixin, DeleteView, UserPassesTestMixin):
    """Delete existing and logged in user.
    The user can only edit himself."""
    model = User
    template_name = 'delete.html'
    extra_context = {
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully deleted')
    denied_url = reverse_lazy('login')
    denied_message = _('You are not logged in! Please log in.')
    permission_denied_message = _('You have no rights to change another user.')

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not request.user.is_authenticated:
            messages.error(self.request, self.denied_message)
            return redirect(self.denied_url)
        elif not user_test_result:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.get_object() == self.request.user
