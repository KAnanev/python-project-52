import pytest
from django.urls import reverse


URL = reverse('login')


@pytest.fixture
def response_login(client):
    response = client.get(URL)
    return response


@pytest.fixture
def response_login_login(client_with_login_test_user_1):
    response = client_with_login_test_user_1.get(URL)
    return response


def test_login_view(response_login):
    assert response_login.status_code == 200
    assert response_login.context['title'] == 'Вход'
    assert '<title>Вход</title>' in response_login.content.decode('utf8')
    assert '<button class="btn btn-primary" type="submit">Войти</button>' in response_login.content.decode('utf8')


def test_login(client, create_test_user_1):
    response = client.post(
        reverse('login'),
        {
            'username': 'test_user_1',
            'password': 'test_pass',
        }, follow=True)
    message = list(response.context.get('messages'))[0]

    assert response.context['user'].is_active
    assert 'Вы залогинены' in message.message
    assert response.templates[0].name == 'index.html'


def test_logout(client_with_login_test_user_1):
    response = client_with_login_test_user_1.post(reverse('logout'), follow=True)

    message = list(response.context.get('messages'))[0]

    assert not response.context['user'].is_active
    assert 'Вы разлогинены' in message.message
    assert response.templates[0].name == 'index.html'
