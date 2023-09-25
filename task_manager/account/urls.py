from django.urls import path
from task_manager.account.views import UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    # path('create/'),
    # path('<int:pk>/update/'),
    # path('<int:pk>/delete/'),
]
