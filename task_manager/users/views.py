from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView

from task_manager.mixins import (
    AuthRequiredMixin, UserPermissionMixin, DeleteViewMixin
)
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserListView(ListView):
    model = User
    template_name = 'users.html'

    extra_context = {
        'title': 'Пользователи',
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'

    success_message = _('Пользователь успешно зарегистрирован')
    success_url = reverse_lazy('login')

    extra_context = {
        'title': _('Регистрация'),
        'button_text': _('Зарегистрировать'),
    }


class UserUpdateView(
    AuthRequiredMixin,
    UserPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    form_class = UserForm
    template_name = 'form.html'

    success_url = reverse_lazy('login')
    permission_url = reverse_lazy('users')

    success_message = _('Пользователь успешно изменен')
    permission_message = _(
        _('У вас нет прав для изменения другого пользователя.')
    )

    extra_context = {
        'title': _('Изменение пользователя'),
        'button_text': _('Изменить'),
    }


class UserDeleteView(
    AuthRequiredMixin,
    UserPermissionMixin,
    SuccessMessageMixin,
    DeleteViewMixin,
):
    model = User

    success_url = reverse_lazy('users')
    permission_url = reverse_lazy('users')

    success_message = _('Пользователь успешно удален')
    permission_message = _(
        _('У вас нет прав для изменения другого пользователя.')
    )

    extra_context = {
        'title': _('Удаление пользователя'),
        'button_text': _('Да, удалить'),
    }
