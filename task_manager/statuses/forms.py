from django.forms import ModelForm

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    """Form for status creation."""
    class Meta:
        model = Status
        fields = ['name']
