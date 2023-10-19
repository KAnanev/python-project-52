import pytest
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from task_manager.tasks.models import Task
from task_manager.users.models import User


class BaseTask:
    url = None
    title = None

    @pytest.fixture
    def response(self, client):
        return client.get(self.url)

    @pytest.fixture
    def post_response(self, client):
        def inner(*args, **kwargs):
            return client.post(*args, **kwargs)
        return inner

    @staticmethod
    def test_view_tasks_without_login(response):
        assert response.status_code == 302
        assert response['Location'] == reverse('login')

    def test_view_tasks_with_login(self, login_user_a, response):
        assert response.status_code == 200
        assert response.context['title'] == self.title
        assert f'<title>{self.title}</title>' in response.content.decode('utf8')


class TestViewTasks(BaseTask):
    url = reverse('tasks')
    title = 'Задачи'


class TestCreateTask(BaseTask):
    url = reverse('create_task')
    title = 'Создать задачу'

    def test_create_task_without_login(self, response):
        super().test_view_tasks_without_login(response)

    def test_create_task_with_login(self, login_user_a, response):
        super().test_view_tasks_with_login(login_user_a, response)

    def test_post_create(self, login_user_a, status_in_db, post_response):
        status = TaskStatus.objects.first()
        user = User.objects.first()
        response = post_response(
            self.url, {
                'name': 'Задача',
                'status': status.pk,
                'executor': user.pk,
            }
            , follow=True
        )

        assert response.status_code == 200

        task = Task.objects.first()
        assert task.status == status
        assert task.executor == user

        message = list(response.context.get('messages'))[0]
        assert 'Задача успешно создана' in message.message
