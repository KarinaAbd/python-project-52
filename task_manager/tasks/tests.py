from django.contrib.messages.storage.cookie import CookieStorage
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.test import get_fixture_content
from task_manager.users.models import User


class TaskTestCase(TestCase):
    """Test case for CRUD of tasks."""
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    test_data = get_fixture_content('test_data.json')
    task_data = test_data['test_task'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.task_count = Task.objects.count()
        self.login_user = User.objects.last()
        self.client.force_login(self.login_user)

    def test_create_task(self) -> None:
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(reverse('task_create'),
                                    data=self.task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        task = Task.objects.last()
        self.assertEqual(task.name, self.task_data['name'])
        self.assertEqual(task.description, self.task_data['description'])
        self.assertEqual(task.author, self.login_user)
        self.assertEqual(task.status,
                         Status.objects.get(id=self.task_data['status']))
        self.assertEqual(task.executor,
                         User.objects.get(id=self.task_data['executor']))
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Task is successfully created'),
                      messages_container)

    def test_list_task(self) -> None:
        self.client.post(reverse('task_create'),
                         data=self.task_data)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/tasks.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Status'), status_code=200)
        self.assertContains(response, _('Author'), status_code=200)
        self.assertContains(response, _('Executor'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, self.task_data['name'])
        self.assertContains(response, self.login_user)
        self.assertContains(response, self.task_data['executor'])
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_page_task(self) -> None:
        self.client.post(reverse('task_create'),
                         data=self.task_data)
        task = Task.objects.last()

        response = self.client.get(reverse('task_page',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_page.html')
        self.assertContains(response, _('Status'), status_code=200)
        self.assertContains(response, _('Author'), status_code=200)
        self.assertContains(response, _('Executor'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, _('Labels'), status_code=200)
        self.assertContains(response, self.task_data['name'])
        self.assertContains(response, self.task_data['description'])
        self.assertContains(response, self.login_user)
        self.assertContains(response, self.task_data['executor'])
        self.assertContains(response, self.task_data['status'])
        label_1 = Label.objects.get(id=self.task_data['labels'][0])
        label_2 = Label.objects.get(id=self.task_data['labels'][1])
        self.assertContains(response, label_1)
        self.assertContains(response, label_2)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_task(self) -> None:
        self.client.post(reverse('task_create'),
                         data=self.task_data)
        task = Task.objects.last()
        response = self.client.get(reverse('task_update',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            {
                'name': 'Rewrite tests before 6pm',
                'description': self.task_data['description'],
                'status': self.task_data['status'],
                'executor': self.task_data['executor'],
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Rewrite tests before 6pm')
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Task is successfully updated'),
                      messages_container)

    def test_delete_task(self) -> None:
        self.client.post(reverse('task_create'),
                         data=self.task_data)
        task = Task.objects.last()
        response = self.client.get(reverse('task_delete',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/delete.html')

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertNotContains(response, self.task_data['name'],
                               status_code=302)
        self.assertEqual(Task.objects.count(), self.task_count)
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Task is successfully deleted'),
                      messages_container)
