from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    """Test case for CRUD of labels."""

    def setUp(self) -> None:
        self.client = Client()
        user = User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )

        self.client.force_login(user)

    def test_create_label(self) -> None:
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('label_create'),
            {'name': 'TEST_label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label = Label.objects.last()
        self.assertEqual(label.name, 'TEST_label')

    def test_list_label(self) -> None:
        Label.objects.create(name='TEST_label')
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, 'TEST_label', status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_label(self) -> None:
        label = Label.objects.create(name='TEST_label')
        response = self.client.get(reverse('label_update',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}),
            {'name': 'TEST_updated_label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'TEST_updated_label')

    def test_delete_label(self) -> None:
        label = Label.objects.create(name='TEST_label')
        response = self.client.get(reverse('label_delete',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        self.assertNotContains(response, 'TEST_label', status_code=302)
        self.assertEqual(Label.objects.count(), 0)
