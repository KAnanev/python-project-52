from django.urls import reverse

from task_manager.users.models import User


def test_without_login_update_user(client, create_test_user_1):
    """Неавторизованный пользователь не может изменять пользователей."""
    user = User.objects.first()
    url = reverse('update_user', kwargs={'pk': user.pk})
    response = client.get(url, follow=True)

    message = list(response.context.get('messages'))[0]

    assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message


def test_login_update_user(client_with_login_test_user_1, create_test_user_2, create_test_user_1):
    """Авторизованный пользователь может изменять только свои данные."""
    users = User.objects.all()
    user_1 = users[0]
    user_2 = users[1]
    url = reverse('update_user', kwargs={'pk': user_2.pk})
    response = client_with_login_test_user_1.get(url, follow=True)

    message = list(response.context.get('messages'))[0]

    assert 'У вас нет прав для изменения другого пользователя.' in message.message

    url = reverse('update_user', kwargs={'pk': user_1.pk})
    response = client_with_login_test_user_1.get(url, follow=True)

    assert response.context['title'] == "Изменение пользователя"
