import pytest
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from task_manager.tasks.models import Task


class TestUserMixin:

    TEST_USER_NAME = 'test_user'
    TEST_PASS = 'test_pass'

    @pytest.fixture
    def test_user_create(self, django_user_model):
        return django_user_model.objects.create_user(
            username=self.TEST_USER_NAME,
            password=self.TEST_PASS
        )


@pytest.fixture
def status_data():
    return {
        'name': 'В работе',
    }


@pytest.fixture
def create_status(db, status_data):
    status = TaskStatus.objects.create(name=status_data['name'])
    return status


@pytest.fixture
def task_data(create_user_a, create_status):
    return {
        'name': 'Написать письмо',
        'description': 'Написать содержательное письмо',
        'status': create_status.pk,
        'executor': create_user_a.pk,
    }


@pytest.fixture
def create_task(db, task_data):
    task = Task.objects.create(**task_data)
    return task


class BaseTest:
    view_name = None

    def get_url(self, *args, **kwargs):
        return reverse(viewname=self.view_name, args=args, kwargs=kwargs)

    @pytest.fixture
    def client_get(self, client):
        def inner(**kwargs):
            if kwargs.get('pk'):
                return client.get(self.get_url(kwargs.pop('pk')), **kwargs)
            return client.get(self.get_url(), **kwargs)

        return inner

    @pytest.fixture
    def client_post(self, client):
        def inner(**kwargs):
            if kwargs.get('pk'):
                return client.post(self.get_url(kwargs.pop('pk')), **kwargs)
            return client.post(self.get_url(), **kwargs)

        return inner


class BaseViewTest:
    title = None
    button_text = None
    error_message = None

    def test_without_login_view(self, client_get):
        """Не авторизованный пользователь, не видит страницу."""

        response = client_get(follow=True)
        message = list(response.context.get('messages'))[0]

        assert response.status_code == 200
        assert self.error_message in message.message

    def test_view(self, login_user_a, client_get):
        """Авторизованный пользователь видит страницу."""

        response = client_get()

        assert response.status_code == 200
        assert response.context['title'] == self.title
        assert f'<title>{self.title}</title>' in response.content.decode('utf8')
        assert self.button_text in response.content.decode('utf8')


class BaseCreateTest:
    view_name = None
    title = None
    button_text = None
    post_data = None
    create_success_message = None

    def test_get_create_view(self, login_user_a, client_get):
        """Тест страницы создания."""
        response = client_get()

        assert response.status_code == 200
        assert response.context['title'] == self.title
        assert f'<title>{self.title}</title>' in response.content.decode('utf8')

    def test_post_create_view(self, login_user_a, client_post):
        """Тест создания."""

        response = client_post(data=self.post_data, follow=True)
        message = list(response.context.get('messages'))[0]
        status = TaskStatus.objects.first()

        assert response.status_code == 200
        assert 'Статус успешно создан' in message.message
        assert status.name == self.post_data.name
