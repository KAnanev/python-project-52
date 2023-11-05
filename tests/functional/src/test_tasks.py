import pytest
from django.urls import reverse


class TestTasksView:
    @pytest.mark.parametrize('url',
                             [
                                 reverse('tasks'),
                                 reverse('create_task'),
                                 #  reverse('update_task', kwargs={'pk': 1}),
                                 #  reverse('delete_tasks', kwargs={'pk': 1}),
                             ])
    def test_statuses_view_without_login(self, url, client):
        """Неавторизованный пользователь перенаправляется в login."""

        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')

        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert response.context['title'] == 'Вход'

# class TestCreateTask(BaseTask):
#     url = reverse('create_task')
#     title = 'Создать задачу'
#
#     def test_create_task_without_login(self, response):
#         super().test_view_tasks_without_login(response)
#
#     def test_create_task_with_login(self, login_user_a, response):
#         super().test_view_tasks_with_login(login_user_a, response)
#
#     def test_post_create(self, login_user_a, status_in_db, post_response):
#         status = TaskStatus.objects.first()
#         user = User.objects.first()
#         response = post_response(
#             self.url, {
#                 'name': 'Задача',
#                 'status': status.pk,
#                 'executor': user.pk,
#             }
#             , follow=True
#         )
#
#         assert response.status_code == 200
#
#         task = Task.objects.first()
#         assert task.status == status
#         assert task.executor == user
#
#         message = list(response.context.get('messages'))[0]
#         assert 'Задача успешно создана' in message.message
