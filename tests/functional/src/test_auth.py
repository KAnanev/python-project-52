from django.urls import reverse
from django.contrib.sessions.models import Session


class TestAuth:

    LOGIN_URL = reverse('login')
    LOGOUT_URL = reverse('logout')

    def test_login_view(self, client):
        """Тест страницы входа."""

        response = client.get(self.LOGIN_URL)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'
        assert '<title>Вход</title>' in response.content.decode('utf8')
        assert '<button class="btn btn-primary" type="submit">Войти</button>' in response.content.decode('utf8')

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
