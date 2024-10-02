from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from tests.conftest import BaseTest, BaseViewTest


class TestStatusesView(BaseViewTest, BaseTest):
    view_name = 'statuses'
    title = 'Статусы'
    button_text = 'Создать статус'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'


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

    def test_get_update_status_view(self, create_status, login_user_a, client_get):
        """Тест страницы обновления статуса."""

        response = client_get(pk=create_status.pk)

        assert response.status_code == 200
        assert response.context['title'] == 'Изменение статуса'
        assert '<title>Изменение статуса</title>' in response.content.decode('utf8')

    def test_post_update_status_view(self, create_status, login_user_a, client_post):
        """Тест обновления статуса."""

        update_status_name = 'Выполнено'
        response = client_post(pk=create_status.pk, data={'name': update_status_name}, follow=True)

        status = TaskStatus.objects.get(pk=create_status.pk)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert status.name == update_status_name
        assert status.name in response.content.decode('utf8')
        assert 'Статус успешно изменен' in message.message


class TestDeleteStatus(BaseTest):
    view_name = 'delete_status'

    def test_get_delete_status(self, create_status, login_user_a, client_get):
        """Тест страницы удаления статуса."""

        response = client_get(pk=create_status.pk)

        assert response.status_code == 200
        assert response.context['title'] == 'Удаление статуса'
        assert 'Да, удалить' in response.content.decode('utf8')
        assert f'Вы уверены, что хотите удалить {create_status.name}?' in response.content.decode('utf8')
        assert 'class="btn btn-danger"' in response.content.decode('utf8')

    def test_post_delete_status(self, create_status, login_user_a, client_post):
        """Тест удаления статуса."""

        response = client_post(pk=create_status.pk, follow=True)
        statuses = TaskStatus.objects.all()
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert not len(statuses)
        assert 'Статус успешно удален' in message.message
