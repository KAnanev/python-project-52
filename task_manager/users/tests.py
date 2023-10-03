from task_manager.users.models import User


def test_model_users(db):
    user = User.objects.create_user(
        username='TestUser', first_name='Test', last_name='User'
    )
    assert 'Test User' == user.get_full_name()
    assert 'TestUser' != user.get_full_name()
