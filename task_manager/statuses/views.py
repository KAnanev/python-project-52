from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.translation import gettext as _

from task_manager.mixins import AuthRequiredMixin, DeleteViewMixin
from task_manager.statuses.models import TaskStatus


class TaskStatusesView(AuthRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses.html'

    extra_context = {
        'title': _('Статусы'),
    }


class TaskStatusMixin(SuccessMessageMixin, AuthRequiredMixin):
    model = TaskStatus
    fields = ('name',)
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')


class TaskStatusCreateView(TaskStatusMixin, CreateView):
    success_message = _('Статус успешно создан')
    extra_context = {
        'title': _('Создать статус'),
        'button_text': _('Создать'),
    }


class TaskStatusUpdateView(TaskStatusMixin, UpdateView):
    success_message = _('Статус успешно изменен')
    extra_context = {
        'title': _('Изменение статуса'),
        'button_text': _('Изменить'),
    }


class TaskStatusDeleteView(TaskStatusMixin, DeleteViewMixin):
    success_message = _('Статус успешно удален')
    extra_context = {
        'title': _('Удаление статуса'),
        'button_text': _('Да, удалить'),
    }
