from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView

from task_manager.mixins import AuthRequiredMixin, DeleteViewMixin
from task_manager.statuses.models import TaskStatus


class TaskStatusesView(AuthRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses.html'

    extra_context = {
        'title': _('Статусы'),
    }


class TaskStatusBaseView(SuccessMessageMixin, AuthRequiredMixin):
    model = TaskStatus
    fields = ('name',)
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')

    success_message = None
    title = None
    button_text = None

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, ** kwargs)
        context['title'] = self.title
        context['button_text'] = self.button_text
        return context


class TaskStatusCreateView(TaskStatusBaseView, CreateView):
    success_message = _('Статус успешно создан')
    title = _('Создать статус')
    button_text = _('Создать')


class TaskStatusUpdateView(TaskStatusBaseView, UpdateView):
    success_message = _('Статус успешно изменен')
    title = _('Изменение статуса')
    button_text = _('Изменить')


class TaskStatusDeleteView(TaskStatusBaseView, DeleteViewMixin):
    success_message = _('Статус успешно удален')
    title = _('Удаление статуса')
    button_text = _('Да, удалить')
