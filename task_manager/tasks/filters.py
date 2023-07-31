from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all())
    executor = ModelChoiceFilter(queryset=User.objects.all())
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_("Label"))
    self_tasks = BooleanFilter(
        label=_('Only own tasks'),
        widget=CheckboxInput,
        method='filter_own_tasks'
    )

    def filter_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
