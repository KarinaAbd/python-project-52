from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name=_('Status name')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date')
    )

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')