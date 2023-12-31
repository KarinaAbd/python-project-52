from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (EntityProtectedMixin, ProjectFormMixin,
                                 ProjectLoginRequiredMixin)
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(ProjectLoginRequiredMixin, ListView):
    """
    List of all statuses.
    Authorization required.
    """
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(ProjectLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    """
    Create new status.
    Authorization required.
    """
    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status is successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(ProjectLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    """
    Update existing status.
    Authorization required.
    """
    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status is successfully updated')
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update'),
    }


class StatusDeleteView(ProjectLoginRequiredMixin,
                       ProjectFormMixin,
                       EntityProtectedMixin,
                       SuccessMessageMixin,
                       DeleteView):
    """
    Delete existing status.
    Authorization required.
    The status can be deleted only if it isn't being used.
    """
    model = Status
    template_name = 'layouts/delete.html'
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('status_list')
    success_message = _('Status is successfully deleted')
    denied_url = reverse_lazy('status_list')
    protected_message = _('Unable to delete a status because it is being used')
