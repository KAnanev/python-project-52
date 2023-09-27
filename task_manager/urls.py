from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from task_manager.views import IndexView, UserLoginView, UserLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name="home"),

    path('admin/', admin.site.urls),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('users/', include('task_manager.account.urls'), name="users"),
]
