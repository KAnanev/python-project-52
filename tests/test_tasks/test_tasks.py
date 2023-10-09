from django.urls import reverse


class TestViewTasks:

    url = reverse('tasks')
    title = 'Задачи'

    def test_view_tasks_without_login(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert response['Location'] == reverse('login')

    def test_view_tasks_with_login(self, client_with_login_test_user_1, client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.context['title'] == self.title
        assert f'<title>{self.title}</title>' in response.content.decode('utf8')


