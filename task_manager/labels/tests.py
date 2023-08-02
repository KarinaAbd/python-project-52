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
    fixtures = ['time.json',
                'users.json',
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
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(reverse('label_create'),
                                    data=self.label_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label = Label.objects.last()
        self.assertEqual(label.name, self.label_data['name'])
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Label is successfully created')
        )

    def test_list_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels.html')
        self.assertContains(response, _('Name'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(response, self.label_data['name'], status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        label = Label.objects.last()
        response = self.client.get(reverse('label_update',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}),
            {'name': 'BEST_WORK_EVER'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'BEST_WORK_EVER')
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Label is successfully updated')
        )

    def test_delete_label(self) -> None:
        self.client.post(reverse('label_create'),
                         data=self.label_data)
        label = Label.objects.last()
        response = self.client.get(reverse('label_delete',
                                           kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        self.assertNotContains(response, self.label_data['name'],
                               status_code=302)
        self.assertEqual(Label.objects.count(), self.labels_count)
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Label is successfully deleted')
        )


class LabelWrongTestCase(TestCase):
    """Test case for CRUD of label with wrong conditions."""
    fixtures = ['time.json',
                'users.json',
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
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('Unable to delete a label because it is being used')
        )
        self.assertEqual(Label.objects.count(), self.labels_count)
