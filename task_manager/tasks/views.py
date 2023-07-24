from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  DetailView)

from task_manager.mixins import (ProjectLoginRequiredMixin,
                                 ProjectUserPassesTestMixin)
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskListView(ProjectLoginRequiredMixin,
                   ListView):
    """List of all tasks."""
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'


class TaskCreateView(ProjectLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    """
    Create new task.
    Authorization required.
    """
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Create task'),
        'button_text': _('Create'),
    }
    success_url = reverse_lazy('task_list')
    success_message = _('Task is successfully created')

    def form_valid(self, form):
        """Add authorized user as author."""
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(ProjectLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    """
    Update existing task.
    Authorization required.
    """
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Update task'),
        'button_text': _('Update'),
    }
    success_url = reverse_lazy('task_list')
    success_message = _('Task is successfully updated')


class TaskDeleteView(ProjectLoginRequiredMixin,
                     ProjectUserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    """
    Delete existing task.
    Authorization required.
    Task can be deleted only by its author.
    """
    model = Task
    template_name = 'delete.html'
    extra_context = {
        'title': _('Delete task'),
        'name': str(model.name),
        'button_text': _('Yes, delete'),
    }
    success_url = reverse_lazy('task_list')
    success_message = _('Task is successfully deleted')
    denied_url = reverse_lazy('task_list')
    permission_denied_message = _('The task can be deleted only by its author')


class TaskPageView(ProjectLoginRequiredMixin,
                   DetailView):
    """Show details of the task."""
    model = Task
    template_name = 'task_page.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        task = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = task.name
        return context
