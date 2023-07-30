from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.test import get_fixture_content
from task_manager.users.models import User


class UserTestCase(TestCase):
    """Test case for CRUD of user."""
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    test_data = get_fixture_content('test_data.json')
    user_data = test_data['test_user'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.user_count = User.objects.count()

    def test_create_user(self) -> None:
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(reverse('user_create'),
                                    data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        user = User.objects.last()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.username, self.user_data['username'])

    def test_list_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users.html')
        self.assertContains(response, _('Full name'), status_code=200)
        self.assertContains(response, _('Creation date'), status_code=200)
        self.assertContains(
            response,
            f"{self.user_data['first_name']} {self.user_data['last_name']}",
            status_code=200
        )
        self.assertContains(response, self.user_data['username'],
                            status_code=200)
        self.assertContains(response, _('Update'), status_code=200)
        self.assertContains(response, _('Delete'), status_code=200)

    def test_update_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        user = User.objects.last()
        self.client.force_login(user)

        response = self.client.get(reverse('user_update',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'first_name': self.user_data['first_name'],
                'last_name': self.user_data['last_name'],
                'username': 'Vlad',
                'password1': self.user_data['password1'],
                'password2': self.user_data['password2']
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.username, 'Vlad')
        self.assertTrue(user.check_password(self.user_data['password1']))

    def test_delete_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        user = User.objects.last()
        self.client.force_login(user)

        response = self.client.get(reverse('user_delete',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete.html')

        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        self.assertEqual(User.objects.count(), self.user_count)
