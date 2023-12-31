import pytest
from django.urls import reverse

from task_manager.tasks.models import Task
from tests.functional.conftest import TestTasksMixin, TestUserMixin, TestStatusesMixin


class TestTasksView(TestTasksMixin):
    @pytest.mark.parametrize('url',
                             [
                                 reverse('tasks'),
                                 reverse('create_task'),
                                 reverse('update_task', kwargs={'pk': 1}),
                                 reverse('delete_task', kwargs={'pk': 1}),
                             ])
    def test_task_view_without_login(self, url, client, create_test_task):
        """Неавторизованный пользователь перенаправляется в login."""

        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'

    @pytest.mark.parametrize(
        ('url', 'title'),
        [(reverse('tasks'), 'Задачи'),
         (reverse('create_task'), 'Создать задачу'),
         (reverse('update_task', kwargs={'pk': 1}), 'Изменение задачи'),
         (reverse('delete_task', kwargs={'pk': 1}), 'Удаление задачи'),
         ])
    def test_statuses_view_with_login(self, url, title, client, create_test_task, login_test_user):
        """Авторизованный пользователь видит страницы."""

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == title

    @pytest.mark.parametrize('url',
                             [reverse('update_task', kwargs={'pk': 1}),
                              reverse('delete_task', kwargs={'pk': 1})])
    def test_statuses_view_login_without_task(self, url, client, login_test_user):
        """Не найдено, если нет задач."""

        response = client.get(url, follow=True)
        assert response.status_code == 404


class TestStatusCRUD(TestTasksMixin):

    def test_create_task(self, client, login_test_user, create_test_status, create_test_user):
        """Задача создается."""

        new_name = 'new_name'
        url = reverse('create_task')

        response = client.post(url, data={
            'name': new_name,
            'author': create_test_user.pk,
            'status': create_test_status.pk,
        })
        status = Task.objects.first()

        assert response.status_code == 302
        assert response.url == reverse('tasks')
        assert status.name == new_name

        response = client.post(url, data={'name': new_name}, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Задача успешно создана' in message.message

    def test_update_status(self,
                           client, login_test_user, create_test_task,
                           create_test_user, create_test_status):
        """Задача обновляется."""

        new_name = 'new_name'
        url = reverse('update_task', kwargs={'pk': create_test_task.pk})

        response = client.post(url, data={
            'name': new_name,
            'author': create_test_user.pk,
            'status': create_test_status.pk,
        })
        task = Task.objects.first()

        assert response.status_code == 302
        assert response.url == reverse('tasks')
        assert task.name == new_name

        response = client.post(url, data={'name': new_name}, follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert 'Задача успешно изменена' in message.message

    def test_get_delete_status(self, client, login_test_user, create_test_task):
        """Задача требует подтверждение удаления."""

        url = reverse('delete_task', kwargs={'pk': create_test_task.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['title'] == 'Удаление задачи'
        assert 'Да, удалить' in response.content.decode('utf8')
        assert f'Вы уверены, что хотите удалить {create_test_task.name}?' in response.content.decode('utf8')
        assert 'class="btn btn-danger"' in response.content.decode('utf8')

    def test_delete_status(self, client, login_test_user, create_test_task):
        """Задача удаляется."""

        url = reverse('delete_task', kwargs={'pk': create_test_task.pk})
        response = client.post(url, follow=True)
        tasks = Task.objects.all()
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert not len(tasks)
        assert 'Задача успешно удалена' in message.message
