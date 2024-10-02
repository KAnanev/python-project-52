from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView

from task_manager.users.models import User


class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteViewMixin(DeleteView):
    def get_template_names(self):
        return 'confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desc'] = _(f'Вы уверены, что хотите удалить {self.object}?')
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            messages.error(request, _('Невозможно удалить суперпользователя.'))
            return redirect(reverse_lazy('users'))
        return super().dispatch(request, *args, **kwargs)
