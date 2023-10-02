import pytest
from django.urls import reverse


@pytest.fixture
def response_home(client):
    url = reverse('home')
    response = client.get(url)
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
    assert text in response_home.content.decode('utf8')
    assert url in response_home.content.decode('utf8')