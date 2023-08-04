from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import (EntityProtectedMixin, ProjectFormMixin,
                                 ProjectLoginRequiredMixin)


class LabelListView(ProjectLoginRequiredMixin, ListView):
    """
    List of all labels.
    Authorization required.
    """
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'


class LabelCreateView(ProjectLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    """
    Create new label.
    Authorization required.
    """
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label is successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(ProjectLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    """
    Update existing label.
    Authorization required.
    """
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label is successfully updated')
    extra_context = {
        'title': _('Update label'),
        'button_text': _('Update'),
    }


class LabelDeleteView(ProjectLoginRequiredMixin,
                      ProjectFormMixin,
                      EntityProtectedMixin,
                      SuccessMessageMixin,
                      DeleteView):
    """
    Delete existing label.
    Authorization required.
    The label can be deleted only if it isn't being used.
    """
    model = Label
    template_name = 'delete.html'
    extra_context = {
        'title': _('Delete label'),
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('label_list')
    success_message = _('Label is successfully deleted')
    denied_url = reverse_lazy('label_list')
    protected_message = _('Unable to delete a label because it is being used')
