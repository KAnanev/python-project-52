from django.urls import reverse

from task_manager.statuses.models import TaskStatus


def test_get_delete_status(status_in_db, client_with_login_test_user_1, client):
    status = TaskStatus.objects.first()
    response = client.get(reverse('delete_status', kwargs={'pk': status.pk}))

    assert response.status_code == 200
    assert response.context['title'] == 'Удаление статуса'
    assert 'Да, удалить' in response.content.decode('utf8')
    assert f'Вы уверены, что хотите удалить {status.name}?' in response.content.decode('utf8')
    assert 'class="btn btn-danger"' in response.content.decode('utf8')


def test_post_delete_status(status_in_db, client_with_login_test_user_1, client):
    status = TaskStatus.objects.first()
    response = client.post(
        reverse('delete_status', kwargs={'pk': status.pk}),
        follow=True
    )

    statuses = TaskStatus.objects.all()
    message = list(response.context.get('messages'))[0]

    assert response.status_code == 200
    assert not len(statuses)
    assert 'Статус успешно удален' in message.message
