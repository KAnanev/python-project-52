from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.translation import gettext as _

from task_manager.mixins import AuthRequiredMixin
from task_manager.statuses.models import TaskStatus


class TaskStatusesView(AuthRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses.html'

    extra_context = {
        'title': _('Статусы'),
    }


class TaskStatusesCreateView(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    model = TaskStatus
    fields = ('name',)
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно создан')

    extra_context = {
        'title': _('Создать статус'),
        'button_text': _('Создать'),
    }
