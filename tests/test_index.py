import pytest


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


@pytest.mark.parametrize(['text', 'url'], [
    ('Вход', '/login/'),
    ('Регистрация', '/users/create/'),
])
def test_navbar_login_index_view(text, url, client_with_login_test_user_1):
    assert text not in client_with_login_test_user_1.content.decode('utf8')
    assert url not in client_with_login_test_user_1.content.decode('utf8')


@pytest.mark.parametrize(['text', 'url'], [
    ('Статусы', '/statuses/'),
    ('Метки', '/labels/'),
    ('Задачи', '/tasks/'),
])
def test_navbar_login_index_view(text, url, client_with_login_test_user_1):
    assert text in client_with_login_test_user_1.content.decode('utf8')
    assert url in client_with_login_test_user_1.content.decode('utf8')
