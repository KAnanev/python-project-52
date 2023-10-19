import pytest
from django.urls import reverse

from task_manager.users.models import User


class BaseTestUserUpdate:
    view_name = 'update_user'

    def get_url(self, *args, **kwargs):
        return reverse(viewname=self.view_name, args=args, kwargs=kwargs)


class TestViewUserUpdate(BaseTestUserUpdate):

    @pytest.fixture
    def client_get(self, client):
        def inner(**kwargs):
            return client.get(self.get_url(kwargs.pop('pk')), **kwargs)

        return inner

    def test_no_auth_update_view(self, create_user_a, client_get):
        """Неавторизованный пользователь переадресован на страницу авторизации."""

        response = client_get(pk=create_user_a.pk)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = client_get(pk=create_user_a.pk, follow=True)
        assert response.status_code == 200

        message = list(response.context.get('messages'))[0]
        assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message

    def test_auth_update_view(self, login_user_a, create_user_a, client_get):
        """Авторизованный пользователь видит страницу изменения пользователя"""

        response = client_get(pk=create_user_a.pk)

        assert response.status_code == 200
        assert response.context['title'] == "Изменение пользователя"


class TestPostUserUpdate(BaseTestUserUpdate):

    @pytest.fixture
    def client_post(self, client):
        def inner(**kwargs):
            return client.post(self.get_url(kwargs.pop('pk')), **kwargs)

        return inner

    @pytest.fixture
    def update_user_a(self, user_a):
        user_a['username'] = 'new_name'
        return user_a

    def test_update_user(self, update_user_a, client_post, login_user_a, create_user_a):
        """Пользователь изменяет свои данные"""

        response = client_post(pk=create_user_a.pk, data=update_user_a, follow=True)

        user = User.objects.first()

        assert response.status_code == 200
        assert not response.context['form'].errors
        assert update_user_a['username'] == user.username

    def test_update_user_another_user(self, update_user_a, client_post, login_user_b, create_user_a, create_user_b):
        """Пользователь может изменять только свои данные"""

        response = client_post(pk=create_user_a.pk, data=update_user_a, follow=True)
        assert response.status_code == 200

        user = User.objects.get(pk=create_user_a.pk)
        assert user.username == update_user_a.get('username')

        message = list(response.context.get('messages'))[0]
        assert 'У вас нет прав для изменения другого пользователя.' in message.message
