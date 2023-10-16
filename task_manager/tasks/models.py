from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import TaskStatus
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        verbose_name=_('Имя'),
    )

    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name=_('Описание')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Автор'),
    )

    executor = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Исполнитель')
    )

    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('Статус')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')
