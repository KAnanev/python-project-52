from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.account.forms import CreateUserForm


class UserListView(ListView):
    model = User
    template_name = 'users.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    success_message = 'Пользователь успешно зарегистрирован'
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    extra_context = {
        'button_text': 'Зарегистрировать',
    }
