import pytest
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.test import TestCase

from task_manager.users.models import User


class TestAuth(TestCase):

    fixtures = ['tests/functional/fixtures/users.json']

    LOGIN_URL = reverse('login')
    LOGOUT_URL = reverse('logout')

    @pytest.fixture
    def client(self, client):
        return client


    def test_login_view(self):
        """Тест страницы входа."""

        response = self.client.get(self.LOGIN_URL)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'
        assert '<title>Вход</title>' in response.content.decode('utf8')
        assert '<button class="btn btn-primary" type="submit">Войти</button>' in response.content.decode('utf8')

        users = User.objects.all()
        assert users.count() == 2

    def test_login(self, user_a, client, create_user_a):
        """Пользователь залогинился."""

        response = client.post(
            self.LOGIN_URL, {
                'username': user_a['username'],
                'password': user_a['password1'],
            }, follow=True
        )
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert response.context['user'].is_active
        assert 'Вы залогинены' in message.message
        assert Session.objects.count() == 1

    def test_logout(self, client, login_user_a):
        """Пользователь разлогинился."""

        response = client.post(reverse('logout'), follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert not response.context['user'].is_active
        assert 'Вы разлогинены' in message.message
        assert not Session.objects.exists()
