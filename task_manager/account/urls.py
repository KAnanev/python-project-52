from django.urls import path
from task_manager.account.views import UserListView, UserCreateView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='signup'),
    # path('<int:pk>/update/'),
    # path('<int:pk>/delete/'),
]
