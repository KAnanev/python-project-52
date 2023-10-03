import pytest
from django.urls import reverse


@pytest.fixture
def response_home(client):
    url = reverse('home')
    response = client.get(url)
    return response


@pytest.fixture
def response_login_home(client_with_login_test_user_1):
    url_ = reverse('home')
    response = client_with_login_test_user_1.get(url_)
    return response


def test_index_view(response_home):
    assert response_home.status_code == 200
    assert response_home.context['title'] == 'Менеджер задач Hexlet'
    assert '<title>Менеджер задач Hexlet</title>' in response_home.content.decode('utf8')


@pytest.mark.parametrize(['text', 'url'], [
    ('Пользователи', '/users/'),
    ('Вход', '/login/'),
    ('Регистрация', '/users/create/'),
])
def test_navbar_index_view(text, url, response_home):
    """Не вошедший пользователь видит вход и регистрацию."""
    assert text in response_home.content.decode('utf8')
    assert url in response_home.content.decode('utf8')


@pytest.mark.parametrize(['text', 'url'], [
    ('Вход', '/login/'),
    ('Регистрация', '/users/create/'),
])
def test_navbar_login_index_view(text, url, response_login_home):
    """Вошедший пользователь не видит вход и регистрацию."""
    assert text not in response_login_home.content.decode('utf8')
    assert url not in response_login_home.content.decode('utf8')


@pytest.mark.parametrize(['text', 'url'], [
    ('Статусы', '/statuses/'),
    ('Метки', '/labels/'),
    ('Задачи', '/tasks/'),
])
def test_navbar_login_index_view_not(text, url, response_login_home):
    """Вошедший пользователь не видит статусы, метки, задачи."""
    assert text in response_login_home.content.decode('utf8')
    assert url in response_login_home.content.decode('utf8')
