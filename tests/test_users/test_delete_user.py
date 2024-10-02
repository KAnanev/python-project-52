from task_manager.users.models import User
from tests.conftest import BaseTest


class BaseTestUserDelete(BaseTest):
    view_name = 'delete_user'


class TestViewUserUpdate(BaseTestUserDelete):

    def test_without_login_delete_user(self, client_post, create_user_a):
        """Неавторизованный пользователь не может удалять пользователей."""

        response = client_post(pk=create_user_a.pk, follow=True)
        message = list(response.context.get('messages'))[0]
        assert response.status_code == 200
        assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message

    def test_login_delete_user(self, login_user_a, client_post,  create_user_a, create_user_b):
        """Авторизованный пользователь может удалять только свои данные."""

        response = client_post(pk=create_user_b.pk, follow=True)
        message = list(response.context.get('messages'))[0]
        assert response.status_code == 200
        assert 'У вас нет прав для изменения другого пользователя.' in message.message

    def test_delete_user(self, client_get, client_post, login_user_a, create_user_a):

        response = client_get(pk=create_user_a.pk)
        assert response.status_code == 200
        assert f"Вы уверены, что хотите удалить {create_user_a.get_full_name()}" in response.context['desc']

        response = client_post(pk=create_user_a.pk, follow=True)
        assert response.status_code == 200

        users = User.objects.all()
        assert users.count() == 0

class TestSuperUserDelete(BaseTestUserDelete):

    def test_delete_super_user(self, client_get, client_post, create_superuser, login_super_user):

        response = client_get(pk=create_superuser.pk)
        assert response.status_code == 302

        response = client_get(pk=create_superuser.pk, follow=True)
        message = list(response.context.get('messages'))[0]
        assert response.status_code == 200
        assert 'Невозможно удалить суперпользователя.' in message.message

        users = User.objects.all()
        assert users.count() == 1
