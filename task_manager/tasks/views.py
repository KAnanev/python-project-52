from django.views.generic.base import TemplateView

from task_manager.mixins import AuthRequiredMixin


class TasksView(AuthRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'tasks.html'

    extra_context = {
        'title': 'Задачи',
        'object_heads': [
            'ID', 'Имя', 'Статус', 'Автор', 'Исполнитель', 'Дата создания',
        ]
    }
