import pytest
from django.urls import reverse


class TestViewUserUpdate:

    @pytest.fixture
    def get_update_user_url(self, client):
        def inner(pk, **kwargs):
            return client.get(reverse('update_user', kwargs={'pk': pk}), **kwargs)

        return inner

    def test_no_auth_update_view(self, test_user_1, get_update_user_url):
        """Неавторизованный пользователь переадресован на страницу авторизации."""
        response = get_update_user_url(test_user_1.pk)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = get_update_user_url(test_user_1.pk, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message

    def test_auth_update_view(self, login_test_user_1, test_user_1, get_update_user_url):
        """Авторизованный пользователь видит страницу изменения пользователя"""
        response = get_update_user_url(test_user_1.pk)

        assert response.status_code == 200
        assert response.context['title'] == "Изменение пользователя"


class TestPostUserUpdate:

    def test_update_user(self, client, login_test_user_1, test_user_1):
        """Пользователь изменяет свои данные"""
        url = reverse('update_user', kwargs={'pk': test_user_1.pk})
        response = client.post(url, {'name': 'change_name'}, follow=True)
        assert response.status_code == 200



def test_login_update_user(login_test_user_1, test_user_2, test_user_1):
    """Авторизованный пользователь может изменять только свои данные."""

    url = reverse('update_user', kwargs={'pk': test_user_2.pk})
    response = login_test_user_1.get(url, follow=True)

    message = list(response.context.get('messages'))[0]

    assert 'У вас нет прав для изменения другого пользователя.' in message.message

    url = reverse('update_user', kwargs={'pk': test_user_1.pk})
    response = login_test_user_1.get(url, follow=True)

    assert response.context['title'] == "Изменение пользователя"
