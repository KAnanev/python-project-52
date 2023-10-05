from django.urls import path
from task_manager.statuses.views import TaskStatusesView

urlpatterns = [
    path('', TaskStatusesView.as_view(), name='statuses'),
]
