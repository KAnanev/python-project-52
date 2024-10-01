import pytest
from task_manager.users.models import User

@pytest.fixture
def create_superuser(db):
    user = User.objects.create_superuser(
        username='superuser',
        email='uperuser@example.com',
        password='superpass'
    )
    return user


@pytest.fixture
def login_super_user(client, create_user_a, create_superuser):
    return client.force_login(create_superuser)