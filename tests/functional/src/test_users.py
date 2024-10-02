import pytest
from django.urls import reverse

from task_manager.users.models import User
from tests.functional.conftest import BaseTest, TestUserMixin


class TestUserView(TestUserMixin):

    def test_user_view(self, db, client):
        """Можно увидеть страницу пользователей."""
        response = client.get(reverse('users'))
        assert response.status_code == 200
        assert response.context['title'] == 'Пользователи'

    @pytest.mark.parametrize('url',
                             [
                                 # reverse('users'),
                                 reverse('update_user', kwargs={'pk': 1}),
                                 reverse('delete_user', kwargs={'pk': 1}),
                             ])
    def test_user_view_without_login(self, url, client, create_test_user):
        """Неавторизованный пользователь переадресован на страницу авторизации."""

        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'

    @pytest.mark.parametrize(('url', 'title'),
                             [
                                 # (reverse('users'), 'Пользователи'),
                                 (reverse('update_user', kwargs={'pk': 1}), 'Изменение пользователя'),
                                 (reverse('delete_user', kwargs={'pk': 1}), 'Удаление пользователя'),
                             ])
    def test_user_view_with_login(self, url, title, client, login_test_user):
        """Авторизованный пользователь видит страницу изменения пользователя"""

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == title

# TODO
# class TestPostUserUpdate:
#
#     @pytest.fixture
#     def update_user_a(self, user_a):
#         user_a['username'] = 'new_name'
#         return user_a
#
#     def test_update_user(self, update_user_a, client_post, login_user_a, create_user_a):
#         """Пользователь изменяет свои данные"""
#
#         response = client_post(pk=create_user_a.pk, data=update_user_a, follow=True)
#         user = User.objects.first()
#
#         assert response.status_code == 200
#         assert not response.context['form'].errors
#         assert update_user_a['username'] == user.username
#
#     def test_update_user_another_user(self, update_user_a, client_post, login_user_b, create_user_a, create_user_b):
#         """Пользователь может изменять только свои данные"""
#
#         response = client_post(pk=create_user_a.pk, data=update_user_a, follow=True)
#         assert response.status_code == 200
#
#         user = User.objects.get(pk=create_user_a.pk)
#         assert user.username == update_user_a.get('username')
#
#         message = list(response.context.get('messages'))[0]
#         assert 'У вас нет прав для изменения другого пользователя.' in message.message
#
#
# class BaseTestUserDelete(BaseTest):
#     view_name = 'delete_user'
#
#
# class TestViewUserDelete(BaseTestUserDelete):
#
#     def test_without_login_delete_user(self, client_post, create_user_a):
#         """Неавторизованный пользователь не может удалять пользователей."""
#
#         response = client_post(pk=create_user_a.pk, follow=True)
#         message = list(response.context.get('messages'))[0]
#         assert response.status_code == 200
#         assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message
#
#     def test_login_delete_user(self, login_user_a, client_post, create_user_a, create_user_b):
#         """Авторизованный пользователь может удалять только свои данные."""
#
#         response = client_post(pk=create_user_b.pk, follow=True)
#         message = list(response.context.get('messages'))[0]
#         assert response.status_code == 200
#         assert 'У вас нет прав для изменения другого пользователя.' in message.message
