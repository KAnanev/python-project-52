from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.forms import UserForm
from task_manager.users.models import User


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


class UserUpdateView(
    UserPassesTestMixin, LoginRequiredMixin,
    SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm
    success_message = _('Пользователь успешно изменен')
    login_url = 'login'
    redirect_field_name = 'login'
    success_url = reverse_lazy('login')
    template_name = 'form.html'

    auth_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    permission_message = _(
        _('У вас нет прав для изменения другого пользователя.')
    )
    permission_url = reverse_lazy('users')

    extra_context = {
        'title': _('Изменение пользователя'),
        'button_text': _('Изменить'),
    }

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    template_name = 'users_confirm_delete.html'
    success_url = reverse_lazy('users')

    success_message = _('Пользователь успешно удален')

    login_url = 'login'
    redirect_field_name = 'login'
    auth_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    permission_message = _(
        _('У вас нет прав для изменения другого пользователя.')
    )
    permission_url = reverse_lazy('users')

    extra_context = {
        'button_text': _('Да, удалить'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desc'] = _(f'Вы уверены, что хотите удалить {self.object}')
        return context

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)