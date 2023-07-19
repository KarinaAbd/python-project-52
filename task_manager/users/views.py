from typing import Any
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
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
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully registered')
    extra_context = {
        'button_text': _('Create'),
    }


class UserUpdateView(SuccessMessageMixin, UpdateView):
    """Update the user."""
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully updated')
    extra_context = {
        'button_text': _('Update'),
    }


class UserDeleteView(SuccessMessageMixin, DeleteView):
    """Delete the user."""
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User is successfully deleted')
    extra_context = {
        'button_text': _('Delete'),
    }
