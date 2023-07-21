from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)

from task_manager.mixins import (ProjectLoginRequiredMixin,
                                 ProjectUserPassesTestMixin)
# from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(ProjectLoginRequiredMixin,
                   ListView):
    """List of all tasks."""
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'


class TaskCreateView(ProjectLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    pass


class TaskUpdateView(ProjectLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    pass


class TaskDeleteView(ProjectLoginRequiredMixin,
                     ProjectUserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    pass


class TaskPageView(View):
    pass
