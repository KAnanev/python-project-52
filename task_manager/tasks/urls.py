from django.urls import path
from task_manager.tasks.views import (
    TasksView,
    # UserCreateView,
    # UserUpdateView,
    # UserDeleteView,
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    # path('create/', UserCreateView.as_view(), name='signup'),
    # path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    # path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
]
