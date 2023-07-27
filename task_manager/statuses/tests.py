from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    """Test case for CRUD of status."""

    def setUp(self) -> None:
        self.client = Client()
        user = User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )

        self.client.force_login(user)

    def test_create_status(self) -> None:
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('status_create'),
            {'name': 'TEST_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        status = Status.objects.last()
        self.assertEqual(status.name, 'TEST_status')

    def test_list_status(self) -> None:
        Status.objects.create(name='TEST_status')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, 'TEST_status', status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_status(self) -> None:
        status = Status.objects.create(name='TEST_status')
        response = self.client.get(reverse('status_update',
                                           kwargs={'pk': status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}),
            {'name': 'TEST_updated_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'TEST_updated_status')

    def test_delete_status(self) -> None:
        status = Status.objects.create(name='TEST_status')
        response = self.client.get(reverse('status_delete',
                                           kwargs={'pk': status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        self.assertNotContains(response, 'TEST_status', status_code=302)
        self.assertEqual(Status.objects.count(), 0)
