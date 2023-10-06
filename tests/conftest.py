import pytest
from django.urls import reverse

from task_manager.statuses.models import TaskStatus


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_test_user_1(create_user):
    return create_user(
        username='test_user_1',
        first_name='test_first_name_1',
        last_name='test_last_name_1',
        password='test_pass',
    )


@pytest.fixture
def create_test_user_2(create_user):
    return create_user(
        username='test_user_2',
        first_name='test_first_name_2',
        last_name='test_last_name_2',
        password='test_pass',
    )


@pytest.fixture
def client_with_login_test_user_1(client, create_test_user_1):
    client.login(
        username='test_user_1', password='test_pass'
    )
    return client


@pytest.fixture
def status_in_db(db):
    TaskStatus.objects.create(name='В работе')
