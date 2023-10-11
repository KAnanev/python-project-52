from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        verbose_name=_('Имя'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    users = models.ForeignKey(
        User,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Пользователи'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')
