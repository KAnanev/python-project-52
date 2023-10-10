from django.urls import reverse


class BaseTask:
    url = None
    title = None

    def test_view_tasks_without_login(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert response['Location'] == reverse('login')

    def test_view_tasks_with_login(self, client_with_login_test_user_1, client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.context['title'] == self.title
        assert f'<title>{self.title}</title>' in response.content.decode('utf8')


class TestViewTasks(BaseTask):
    url = reverse('tasks')
    title = 'Задачи'


class TestCreateTask(BaseTask):
    url = reverse('create_tasks')
    title = 'Создать задачу'

    def test_create_task_without_login(self, client):
        super().test_view_tasks_without_login(client)

    def test_create_task_with_login(self, client_with_login_test_user_1, client):
        super().test_view_tasks_with_login(client_with_login_test_user_1, client)
