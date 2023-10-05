from django.views.generic import ListView
from django.utils.translation import gettext as _

from task_manager.mixins import AuthRequiredMixin
from task_manager.statuses.models import TaskStatus


class TaskStatusesView(AuthRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses.html'

    extra_context = {
        'title': _('Статусы'),
    }
