from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from tests.conftest import BaseTest


class TestStatusesView(BaseTest):
    view_name = 'statuses'

    def test_without_login_statuses_view(self, client_get):
        """Не авторизованный пользователь, не видит страницу статусов."""

        response = client_get(follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message

    def test_status_view(self, login_user_a, client_get):
        """Авторизованный пользователь видит страницу статусов."""

        response = client_get()

        assert response.context['title'] == 'Статусы'
        assert '<title>Статусы</title>' in response.content.decode('utf8')
        assert 'Создать статус' in response.content.decode('utf8')


class TestCreateStatus(BaseTest):
    view_name = 'create_status'

    def test_get_create_status_view(self, login_user_a, client_get):
        """Тест страницы создания статуса."""
        response = client_get()

        assert response.status_code == 200
        assert response.context['title'] == 'Создать статус'
        assert '<title>Создать статус</title>' in response.content.decode('utf8')

    def test_post_create_status_view(self, login_user_a, client_post):
        """Тест создания статуса."""
        status_name = 'В работе'

        response = client_post(data={'name': status_name}, follow=True)
        message = list(response.context.get('messages'))[0]
        status = TaskStatus.objects.first()

        assert response.status_code == 200
        assert 'Статус успешно создан' in message.message
        assert status.name == status_name


class TestUpdateStatus(BaseTest):
    view_name = 'update_status'

    def test_get_update_status_view(self, status_in_db, login_user_a, client_get):
        """Тест страницы обновления статуса."""

        response = client_get(pk=status_in_db.pk)

        assert response.status_code == 200
        assert response.context['title'] == 'Изменение статуса'
        assert '<title>Изменение статуса</title>' in response.content.decode('utf8')

    def test_post_update_status_view(self, status_in_db, login_user_a, client_post):
        """Тест обновления статуса."""

        update_status_name = 'Выполнено'
        response = client_post(pk=status_in_db.pk, data={'name': update_status_name}, follow=True)

        status = TaskStatus.objects.get(pk=status_in_db.pk)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert status.name == update_status_name
        assert status.name in response.content.decode('utf8')
        assert 'Статус успешно изменен' in message.message


class TestDeleteStatus(BaseTest):
    view_name = 'delete_status'

    def test_get_delete_status(self, status_in_db, login_user_a, client_get):
        """Тест страницы удаления статуса."""

        response = client_get(pk=status_in_db.pk)

        assert response.status_code == 200
        assert response.context['title'] == 'Удаление статуса'
        assert 'Да, удалить' in response.content.decode('utf8')
        assert f'Вы уверены, что хотите удалить {status_in_db.name}?' in response.content.decode('utf8')
        assert 'class="btn btn-danger"' in response.content.decode('utf8')

    def test_post_delete_status(self, status_in_db, login_user_a, client_post):
        """Тест удаления статуса."""

        response = client_post(pk=status_in_db.pk, follow=True)
        statuses = TaskStatus.objects.all()
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert not len(statuses)
        assert 'Статус успешно удален' in message.message
