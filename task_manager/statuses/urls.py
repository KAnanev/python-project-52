from django.urls import path
from task_manager.statuses.views import (
    TaskStatusesView, TaskStatusCreateView,
    TaskStatusUpdateView,
)

urlpatterns = [
    path('', TaskStatusesView.as_view(), name='statuses'),
    path('create', TaskStatusCreateView.as_view(), name='create_status'),
    path('<int:pk>/update',
         TaskStatusUpdateView.as_view(), name='update_status'),
    path('delete', TaskStatusesView.as_view(), name='delete_status'),
]
