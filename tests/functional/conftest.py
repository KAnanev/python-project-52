import pytest
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from task_manager.tasks.models import Task


class TestUserMixin:

    TEST_USER_NAME = 'test_user'
    TEST_PASS = 'test_pass'

    @pytest.fixture
    def test_user(self):
        return {
            'username': self.TEST_USER_NAME,
            'password': self.TEST_PASS,
        }

    @pytest.fixture
    def create_test_user(self, test_user, django_user_model):
        return django_user_model.objects.create_user(**test_user)

    @pytest.fixture
    def login_test_user(self, test_user, create_test_user, client):
        return client.login(**test_user)


class TestStatusesMixin:
    TEST_STATUS_NAME = 'test_status'

    @pytest.fixture
    def create_test_status(self, db):
        return TaskStatus.objects.create(name=self.TEST_STATUS_NAME)


class TestTasksMixin(TestStatusesMixin, TestUserMixin):
    TEST_TASK_NAME = 'test_task'

    @pytest.fixture
    def create_test_task(self, create_test_status, create_test_user):
        return Task.objects.create(
            name=self.TEST_TASK_NAME,
            author=create_test_user,
            status=create_test_status
        )


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
