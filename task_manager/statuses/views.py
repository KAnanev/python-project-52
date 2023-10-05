from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from task_manager.statuses.models import TaskStatus


class TaskStatusesView(LoginRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses.html'
