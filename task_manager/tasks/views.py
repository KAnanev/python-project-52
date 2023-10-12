from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateView

from task_manager.mixins import AuthRequiredMixin
from task_manager.tasks.models import Task


class TasksView(AuthRequiredMixin, ListView):
    model = Task
    login_url = 'login'
    template_name = 'tasks.html'

    extra_context = {
        'title': 'Задачи',
        'object_table_head': [
            'ID', 'Имя', 'Статус', 'Автор', 'Исполнитель', 'Дата создания',
        ]
    }
