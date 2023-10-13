from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import ContextMixin

from task_manager.mixins import AuthRequiredMixin, DeleteViewMixin
from task_manager.statuses.models import TaskStatus


class TaskStatusBase(AuthRequiredMixin, ContextMixin):
    model = TaskStatus
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class TaskStatusModifiedBase(SuccessMessageMixin, TaskStatusBase):

    fields = ('name',)
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')

    button_text = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = self.button_text
        return context


class TaskStatusesView(TaskStatusBase, ListView):
    title = _('Статусы')
    template_name = 'statuses.html'


class TaskStatusCreateView(TaskStatusModifiedBase, CreateView):
    success_message = _('Статус успешно создан')
    title = _('Создать статус')
    button_text = _('Создать')


class TaskStatusUpdateView(TaskStatusModifiedBase, UpdateView):
    success_message = _('Статус успешно изменен')
    title = _('Изменение статуса')
    button_text = _('Изменить')


class TaskStatusDeleteView(TaskStatusModifiedBase, DeleteViewMixin):
    success_message = _('Статус успешно удален')
    title = _('Удаление статуса')
    button_text = _('Да, удалить')
