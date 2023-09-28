from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from task_manager.account.forms import UserForm
from task_manager.account.models import User


class UserListView(ListView):
    model = User
    template_name = 'users.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_message = _('Пользователь успешно зарегистрирован')
    success_url = reverse_lazy('login')
    template_name = 'form.html'

    extra_context = {
        'title': _('Регистрация'),
        'button_text': _('Зарегистрировать'),
    }


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    success_message = _('Пользователь успешно изменен')
    login_url = 'login'
    redirect_field_name = 'login'
    success_url = reverse_lazy('login')
    template_name = 'form.html'

    extra_context = {
        'title': _('Изменение пользователя'),
        'button_text': _('Изменить'),
    }
