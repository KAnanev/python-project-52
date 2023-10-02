from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'title': _('Менеджер задач Hexlet')}


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home')
    success_message = _('Вы залогинены')
    extra_context = {
        'title:': _('Войти'),
        'button_text': _('Войти'),
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    success_message = _('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
