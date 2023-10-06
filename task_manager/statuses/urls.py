from django.urls import path
from task_manager.statuses.views import TaskStatusesView, TaskStatusesCreateView

urlpatterns = [
    path('', TaskStatusesView.as_view(), name='statuses'),
    path('create', TaskStatusesCreateView.as_view(), name='create_status'),
    path('update', TaskStatusesView.as_view(), name='update_status'),
    path('delete', TaskStatusesView.as_view(), name='delete_status'),
]
