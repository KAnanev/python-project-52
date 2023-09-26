from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('users/', include('task_manager.account.urls')),
    path('admin/', admin.site.urls),
]
