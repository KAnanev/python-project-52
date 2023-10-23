import pytest
from django.urls import reverse

from task_manager.users.models import User
from tests.functional.conftest import BaseTest


class BaseTestUserUpdate(BaseTest):
    view_name = 'update_user'


class TestViewUserUpdate(BaseTestUserUpdate):

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


class BaseTestUserDelete(BaseTest):
    view_name = 'delete_user'


class TestViewUserDelete(BaseTestUserDelete):

    def test_without_login_delete_user(self, client_post, create_user_a):
        """Неавторизованный пользователь не может удалять пользователей."""

        response = client_post(pk=create_user_a.pk, follow=True)
        message = list(response.context.get('messages'))[0]
        assert response.status_code == 200
        assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message

    def test_login_delete_user(self, login_user_a, client_post, create_user_a, create_user_b):
        """Авторизованный пользователь может удалять только свои данные."""

        response = client_post(pk=create_user_b.pk, follow=True)
        message = list(response.context.get('messages'))[0]
        assert response.status_code == 200
        assert 'У вас нет прав для изменения другого пользователя.' in message.message
