import pytest
from django.urls import reverse


URL = reverse('login')


def test_login_view(client):
    """Тест страницы входа."""

    response = client.get(URL)
    assert response.status_code == 200
    assert response.context['title'] == 'Вход'
    assert '<title>Вход</title>' in response.content.decode('utf8')
    assert '<button class="btn btn-primary" type="submit">Войти</button>' in response.content.decode('utf8')


def test_login(user_a, client, login_user_a):
    """Пользователь залогинился."""

    response = client.post(
        reverse('login'),
        {
            'username': user_a['username'],
            'password': user_a['password1'],
        },
        follow=True
    )

    message = list(response.context.get('messages'))[0]

    assert response.context['user'].is_active
    assert 'Вы залогинены' in message.message
    assert response.templates[0].name == 'index.html'


def test_logout(client, login_user_a):
    """Пользователь разлогинился."""

    response = client.post(reverse('logout'), follow=True)

    message = list(response.context.get('messages'))[0]

    assert not response.context['user'].is_active
    assert 'Вы разлогинены' in message.message
    assert response.templates[0].name == 'index.html'
