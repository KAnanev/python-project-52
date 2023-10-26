import pytest
from django.urls import reverse
from django.contrib.sessions.models import Session


class TestAuth:

    LOGIN_URL = reverse('login')
    LOGOUT_URL = reverse('logout')

    TEST_USER_NAME = 'test_user'
    TEST_PASS = 'test_pass'

    @pytest.fixture
    def test_user_create(self, django_user_model):
        return django_user_model.objects.create_user(
            username=self.TEST_USER_NAME,
            password=self.TEST_PASS
        )

    def test_login_view(self, client):
        """Тест страницы входа."""

        response = client.get(self.LOGIN_URL)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'
        assert '<title>Вход</title>' in response.content.decode('utf8')
        assert '<button class="btn btn-primary" type="submit">Войти</button>' in response.content.decode('utf8')

    def test_login(self, test_user_create, client):
        """Пользователь может авторизоваться."""

        response = client.post(
            self.LOGIN_URL, {
                'username': self.TEST_USER_NAME,
                'password': self.TEST_PASS,
            }, follow=True
        )

        assert response.status_code == 200
        assert response.context['user'].is_active

        message = list(response.context.get('messages'))[0]
        assert 'Вы залогинены' in message.message
        assert Session.objects.count() == 1

    def test_logout(self, test_user_create, client):
        """Пользователь может выйти."""

        client.login(username=self.TEST_USER_NAME, password=self.TEST_PASS)

        response = client.post(self.LOGOUT_URL, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert not response.context['user'].is_active
        assert 'Вы разлогинены' in message.message
        assert not Session.objects.exists()
