import pytest
from django.urls import reverse

URL = reverse('statuses')


def test_without_login_statuses_view(client):

    response = client.get(URL)
    assert response.status_code == 302

    response = client.get(URL, follow=True)
    message = list(response.context.get('messages'))[0]

    assert response.status_code == 200
    assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message


def test_statuses_view(client_with_login_test_user_1, client):

    response = client.get(URL)

    assert response.context['title'] == 'Статусы'
    assert '<title>Статусы</title>' in response.content.decode('utf8')
