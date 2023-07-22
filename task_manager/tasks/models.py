from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name=_('Task name')
    )
    description = models.TextField(
        max_length=15000,
        blank=True,
        verbose_name=_('Task description')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author',
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Performer'),
        related_name='performer',
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelationships',
        through_fields=('task', 'label'),
        blank=True,
        verbose_name=_('Labels'),
        related_name='labels'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date')
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelationships(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
