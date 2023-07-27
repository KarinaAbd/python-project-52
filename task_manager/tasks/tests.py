from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    """Test case for CRUD of tasks."""

    def setUp(self) -> None:
        self.client = Client()

        self.user_author = User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )
        self.user_executor = User.objects.create(
            first_name='Peter',
            last_name='Kwill',
            username='StarLord',
            password='qwerty789',
        )
        self.client.force_login(self.user_author)

        self.status = Status.objects.create(name='TEST_status')
        self.label_1 = Label.objects.create(name='TEST_label_1')
        self.label_2 = Label.objects.create(name='TEST_label_2')

    def test_create_task(self) -> None:
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'TEST_Task',
                'description': 'TEST_description',
                'author': self.user_author.id,
                'status': self.status.id,
                'executor': self.user_executor.id,
                'labels': [self.label_1.id, self.label_2.id]
            }
        )

        task = Task.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(task.name, 'TEST_Task')
        self.assertEqual(task.description, 'TEST_description')
        self.assertEqual(task.author, self.user_author)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.user_executor)

    def test_list_task(self) -> None:
        Task.objects.create(
            name='TEST_Task',
            description='TEST_description',
            author=self.user_author,
            status=self.status,
            executor=self.user_executor,
        )
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Status'), status_code=200)
        self.assertContains(response, _('Author'), status_code=200)
        self.assertContains(response, _('Executor'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, 'TEST_Task', status_code=200)
        self.assertContains(response, 'Taika Waititi', status_code=200)
        self.assertContains(response, 'Peter Kwill', status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_page_task(self) -> None:
        task = Task.objects.create(
            name='TEST_Task',
            description='TEST_description',
            author=self.user_author,
            status=self.status,
            executor=self.user_executor,
        )
        task.labels.set([self.label_1, self.label_2])
        response = self.client.get(reverse('task_page',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task_page.html')
        self.assertContains(response, _('Status'), status_code=200)
        self.assertContains(response, _('Author'), status_code=200)
        self.assertContains(response, _('Executor'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, _('Labels'), status_code=200)
        self.assertContains(response, 'TEST_Task', status_code=200)
        self.assertContains(response, 'TEST_description', status_code=200)
        self.assertContains(response, 'Taika Waititi', status_code=200)
        self.assertContains(response, 'Peter Kwill', status_code=200)
        self.assertContains(response, 'TEST_status', status_code=200)
        self.assertContains(response, 'TEST_label_1', status_code=200)
        self.assertContains(response, 'TEST_label_2', status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_task(self) -> None:
        task = Task.objects.create(
            name='TEST_Task',
            description='TEST_description',
            author=self.user_author,
            status=self.status,
            executor=self.user_executor,
        )
        response = self.client.get(reverse('task_update',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            {
                'name': 'TEST_updated_Task',
                'description': 'TEST_description',
                'author': self.user_author.id,
                'status': self.status.id,
                'executor': self.user_executor.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'TEST_updated_Task')
        # self.assertContains(response, 'Taika Waititi', status_code=302)
        # self.assertContains(response, 'Peter Kwill', status_code=302)

    def test_delete_task(self) -> None:
        task = Task.objects.create(
            name='TEST_Task',
            description='TEST_description',
            author=self.user_author,
            status=self.status,
            executor=self.user_executor,
        )
        response = self.client.get(reverse('task_delete',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertNotContains(response, 'TEST_Task', status_code=302)
        self.assertEqual(Task.objects.count(), 0)
