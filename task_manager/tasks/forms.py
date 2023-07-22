from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    """Form for tasks creation."""
    class Meta:
        model = Task
        fields = (
            'name', 'description', 'status', 'executor', 'labels'
        )
