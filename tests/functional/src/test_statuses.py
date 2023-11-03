import pytest
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from tests.functional.conftest import TestStatusesMixin, TestUserMixin


class TestStatusesView(TestStatusesMixin, TestUserMixin):

    @pytest.mark.parametrize('url',
                             [reverse('statuses'),
                              reverse('create_status'),
                              reverse('update_status', kwargs={'pk': 1}),
                              reverse('delete_status', kwargs={'pk': 1})])
    def test_statuses_view_without_login(self, url, client):
        """Неавторизованный пользователь перенаправляется в login."""
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'

    @pytest.mark.parametrize(
        ('url', 'title'),
        [(reverse('statuses'), 'Статусы'),
         (reverse('create_status'), 'Создать статус'),
         (reverse('update_status', kwargs={'pk': 1}), 'Изменение статуса'),
         (reverse('delete_status', kwargs={'pk': 1}), 'Удаление статуса'),
         ])
    def test_statuses_view_with_login(self, url, title, client, create_test_status, login_test_user):
        """Авторизованный пользователь видит страницы"""
        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == title

    @pytest.mark.parametrize('url',
                             [reverse('update_status', kwargs={'pk': 1}),
                              reverse('delete_status', kwargs={'pk': 1})])
    def test_statuses_view_login_without_task(self, url, client, login_test_user):
        """Не найдено, если нет статусов."""
        response = client.get(url, follow=True)
        assert response.status_code == 404


class TestStatusCRUD(TestUserMixin, TestStatusesMixin):

    def test_create_status(self, client, login_test_user):
        """Статус создается."""

        new_name = 'new_name'
        url = reverse('create_status')

        response = client.post(url, data={'name': new_name})
        status = TaskStatus.objects.first()

        assert response.status_code == 302
        assert response.url == reverse('statuses')
        assert status.name == new_name

        response = client.post(url, data={'name': new_name}, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Статус успешно создан' in message.message

    def test_update_status(self, client, login_test_user, create_test_status):
        """Тест обновления статуса."""

        new_name = 'new_name'
        status = TaskStatus.objects.first()
        url = reverse('update_status', kwargs={'pk': status.pk})

        response = client.post(url, data={'name': new_name})
        status = TaskStatus.objects.first()

        assert response.status_code == 302
        assert response.url == reverse('statuses')
        assert status.name == new_name

        response = client.post(url, data={'name': new_name}, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Статус успешно изменен' in message.message
#
#
# class TestDeleteStatus(BaseTest):
#     view_name = 'delete_status'
#
#     def test_get_delete_status(self, create_status, login_user_a, client_get):
#         """Тест страницы удаления статуса."""
#
#         response = client_get(pk=create_status.pk)
#
#         assert response.status_code == 200
#         assert response.context['title'] == 'Удаление статуса'
#         assert 'Да, удалить' in response.content.decode('utf8')
#         assert f'Вы уверены, что хотите удалить {create_status.name}?' in response.content.decode('utf8')
#         assert 'class="btn btn-danger"' in response.content.decode('utf8')
#
#     def test_post_delete_status(self, create_status, login_user_a, client_post):
#         """Тест удаления статуса."""
#
#         response = client_post(pk=create_status.pk, follow=True)
#         statuses = TaskStatus.objects.all()
#         message = list(response.context.get('messages'))[0]
#
#         assert response.status_code == 200
#         assert not len(statuses)
#         assert 'Статус успешно удален' in message.message
