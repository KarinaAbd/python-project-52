from django.contrib.messages.storage.cookie import CookieStorage
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.test import get_fixture_content
from task_manager.users.models import User


class StatusTestCase(TestCase):
    """Test case for CRUD of status."""
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    test_data = get_fixture_content('test_data.json')
    status_data = test_data['test_status'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.status_count = Status.objects.count()
        self.user = User.objects.last()
        self.client.force_login(self.user)

    def test_create_status(self) -> None:
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(reverse('status_create'),
                                    data=self.status_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        status = Status.objects.last()
        self.assertEqual(status.name, self.status_data['name'])
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Status is successfully created')
        )

    def test_list_status(self) -> None:
        self.client.post(reverse('status_create'),
                         data=self.status_data)
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, self.status_data['name'],
                            status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_status(self) -> None:
        self.client.post(reverse('status_create'),
                         data=self.status_data)
        status = Status.objects.last()
        response = self.client.get(reverse('status_update',
                                           kwargs={'pk': status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}),
            {'name': 'RUNNING TESTS again'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'RUNNING TESTS again')
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Status is successfully updated')
        )

    def test_delete_status(self) -> None:
        self.client.post(reverse('status_create'),
                         data=self.status_data)
        status = Status.objects.last()
        response = self.client.get(reverse('status_delete',
                                           kwargs={'pk': status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        self.assertNotContains(response, self.status_data['name'],
                               status_code=302)
        self.assertEqual(Status.objects.count(), self.status_count)
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Status is successfully deleted')
        )


class StatusWrongTestCase(TestCase):
    """Test case for CRUD of status with wrong conditions."""
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    def setUp(self) -> None:
        self.client = Client()
        self.status_count = Status.objects.count()
        self.user = User.objects.last()
        self.client.force_login(self.user)

    def test_delete_used_status(self) -> None:
        task = Task.objects.last()
        response = self.client.post(reverse('status_delete',
                                            kwargs={'pk': task.status.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Unable to delete a status because it is being used')
        )
        self.assertEqual(Status.objects.count(), self.status_count)
