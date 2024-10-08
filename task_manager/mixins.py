from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView


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
        user = self.get_object()
        return (
            user == self.request.user and not self.request.user.is_superuser
        ) or (
            self.request.user.is_superuser and user != self.request.user
        )

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
