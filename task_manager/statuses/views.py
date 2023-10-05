from django.shortcuts import render
from django.views.generic import ListView

from task_manager.statuses.models import TaskStatus


class StatusesView(ListView):
    model = TaskStatus
    template_name = 'statuses.html'
