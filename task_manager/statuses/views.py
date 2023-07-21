from django.views.generic import ListView, CreateView
from .forms import StatusForm
from .models import Status
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class StatusListView(ListView):
    """List of all statuses.
    Authorization required."""
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    """Create new status.
    Authorization required."""
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status is successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }
