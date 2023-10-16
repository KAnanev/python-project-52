from django.urls import reverse

from task_manager.statuses.models import TaskStatus

URL = reverse('statuses')
CREATE_STATUSES_URL = reverse('create_status')

STATUS = 'Выполнено'


def test_without_login_statuses_view(client):

    response = client.get(URL)
    assert response.status_code == 302

    response = client.get(URL, follow=True)
    message = list(response.context.get('messages'))[0]

    assert response.status_code == 200
    assert 'Вы не авторизованы! Пожалуйста, выполните вход.' in message.message


def test_status_view(status_in_db, login_test_user_1, client):

    response = client.get(URL)

    assert response.context['title'] == 'Статусы'
    assert '<title>Статусы</title>' in response.content.decode('utf8')
    assert 'Создать статус' in response.content.decode('utf8')
    assert 'В работе' in response.content.decode('utf8')


def test_get_create_status_view(login_test_user_1, client):

    response = client.get(CREATE_STATUSES_URL)
    assert response.status_code == 200
    assert response.context['title'] == 'Создать статус'
    assert '<title>Создать статус</title>' in response.content.decode('utf8')


def test_post_create_status_view(login_test_user_1, client):

    response = client.post(CREATE_STATUSES_URL, {'name': STATUS}, follow=True)
    message = list(response.context.get('messages'))[0]

    assert response.status_code == 200
    assert STATUS in response.content.decode('utf8')
    assert 'Статус успешно создан' in message.message


def test_get_update_status_view(status_in_db, login_test_user_1, client):
    status = TaskStatus.objects.first()
    response = client.get(reverse('update_status', kwargs={'pk': status.pk}))

    assert response.status_code == 200
    assert response.context['title'] == 'Изменение статуса'
    assert '<title>Изменение статуса</title>' in response.content.decode('utf8')
    assert status.name in response.content.decode('utf8')


def test_post_update_status_view(status_in_db, login_test_user_1, client):

    status = TaskStatus.objects.first()
    response = client.post(
        reverse('update_status', kwargs={'pk': status.pk}),
        {'name': STATUS},
        follow=True,
    )

    status = TaskStatus.objects.get(pk=status.pk)
    message = list(response.context.get('messages'))[0]

    assert response.status_code == 200
    assert status.name == STATUS
    assert status.name in response.content.decode('utf8')
    assert 'Статус успешно изменен' in message.message
