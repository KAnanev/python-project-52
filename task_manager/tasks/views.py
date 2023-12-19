from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import ContextMixin
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import AuthRequiredMixin, DeleteViewMixin
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TasksView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'

    extra_context = {
        'title': 'Задачи',
        'object_table_head': [
            'ID', 'Имя', 'Статус', 'Автор', 'Исполнитель', 'Дата создания',
        ]
    }


class TaskBaseView(SuccessMessageMixin, AuthRequiredMixin, ContextMixin):
    model = Task
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')

    success_message = None
    title = None
    button_text = None

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['button_text'] = self.button_text
        return context


class TaskCreateView(TaskBaseView, CreateView):

    fields = ('name', 'description', 'status', 'executor')

    success_message = _('Задача успешно создана')
    title = _('Создать задачу')
    button_text = _('Создать')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskBaseView, UpdateView):

    fields = ('name', 'description', 'status', 'executor')

    success_message = _('Задача успешно изменена')
    title = _('Изменение задачи')
    button_text = _('Изменить')


class TaskDeleteView(TaskBaseView, DeleteViewMixin):
    success_message = _('Задача успешно удалена')
    title = _('Удаление задачи')
    button_text = _('Да, удалить')
