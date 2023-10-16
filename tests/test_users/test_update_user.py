from django.urls import reverse


def test_without_login_update_user(client, test_user_1):
    """Неавторизованный пользователь не может изменять пользователей."""

    url = reverse('update_user', kwargs={'pk': test_user_1.pk})
    response = client.get(url, follow=True)

    message = list(response.context.get('messages'))[0]

    assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message


def test_login_update_user(login_test_user_1, test_user_2, test_user_1):
    """Авторизованный пользователь может изменять только свои данные."""

    url = reverse('update_user', kwargs={'pk': test_user_2.pk})
    response = login_test_user_1.get(url, follow=True)

    message = list(response.context.get('messages'))[0]

    assert 'У вас нет прав для изменения другого пользователя.' in message.message

    url = reverse('update_user', kwargs={'pk': test_user_1.pk})
    response = login_test_user_1.get(url, follow=True)

    assert response.context['title'] == "Изменение пользователя"
