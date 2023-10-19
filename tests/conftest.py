import pytest
from task_manager.statuses.models import TaskStatus


@pytest.fixture
def user_a():
    return {
        'username': 'user_a',
        'first_name': 'first_name_a',
        'last_name': 'last_name_a',
        'password1': 'pass',
        'password2': 'pass',
    }


@pytest.fixture
def user_b():
    return {
        'username': 'test_user_b',
        'first_name': 'test_first_name_b',
        'last_name': 'test_last_name_b',
        'password1': 'pass',
        'password2': 'pass',
    }


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_user_a(user_a, create_user):
    return create_user(username=user_a.get('username'), password=user_a.get('password1'))


@pytest.fixture
def create_user_b(user_b, create_user):
    return create_user(username=user_b.get('username'), password=user_b.get('password1'))


@pytest.fixture
def login_user_a(client, create_user_a):
    return client.force_login(create_user_a)


@pytest.fixture
def login_user_b(client, create_user_b):
    return client.force_login(create_user_b)


@pytest.fixture
def status_in_db(db):
    TaskStatus.objects.create(name='В работе')
