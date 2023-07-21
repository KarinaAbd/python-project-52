from .models import Status
from django.forms import ModelForm


class StatusForm(ModelForm):
    """Form for status creation."""
    class Meta:
        model = Status
        fields = ['name']
