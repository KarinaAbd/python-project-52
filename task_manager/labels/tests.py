from django.contrib.messages.storage.cookie import CookieStorage
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.test import get_fixture_content
from task_manager.users.models import User


class LabelTestCase(TestCase):
    """Test case for CRUD of labels."""
    fixtures = ['users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    test_data = get_fixture_content('test_data.json')
    label_data = test_data['test_label'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.labels_count = Label.objects.count()
        self.user = User.objects.last()
        self.client.force_login(self.user)

    def test_create_label(self) -> None:
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(reverse('label_create'),
                                    data=self.label_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label = Label.objects.last()
        self.assertEqual(label.name, self.label_data['name'])
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Label is successfully created'),
                      messages_container)

    def test_list_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/labels.html')
        self.assertContains(response, _('Name'))
        self.assertContains(response, _('Creation date'))
        self.assertContains(response, self.label_data['name'])
        self.assertContains(response, _('Update'))
        self.assertContains(response, _('Delete'))

    def test_update_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        label = Label.objects.last()
        response = self.client.get(reverse('label_update',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}),
            {'name': 'BEST_WORK_EVER'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'BEST_WORK_EVER')
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Label is successfully updated'),
                      messages_container)

    def test_delete_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        label = Label.objects.last()
        response = self.client.get(reverse('label_delete',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/delete.html')

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        self.assertNotContains(response, self.label_data['name'],
                               status_code=302)
        self.assertEqual(Label.objects.count(), self.labels_count)
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Label is successfully deleted'),
                      messages_container)


class LabelWrongTestCase(TestCase):
    """Test case for CRUD of label with wrong conditions."""
    fixtures = ['users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    def setUp(self) -> None:
        self.client = Client()
        self.labels_count = Label.objects.count()
        self.user = User.objects.last()
        self.client.force_login(self.user)

    def test_delete_used_label(self) -> None:
        task = Task.objects.last()
        labels = task.labels.all()
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': labels[0].id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn(_('Unable to delete a label because it is being used'),
                      messages_container)
        self.assertEqual(Label.objects.count(), self.labels_count)
