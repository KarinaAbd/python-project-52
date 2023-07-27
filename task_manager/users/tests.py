from django.test import Client, TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_create_user(self) -> None:
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('user_create'),
            {
                'first_name': 'Taika',
                'last_name': 'Waititi',
                'username': 'Viago',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        user = User.objects.last()
        self.assertEqual(user.first_name, 'Taika')
        self.assertEqual(user.last_name, 'Waititi')
        self.assertEqual(user.username, 'Viago')

    def test_login_user(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )
        user = User.objects.last()
        response = self.client.post(
            reverse('login'),
            {
                'username': user.username,
                'password': user.password,
            }
        )
        self.assertTrue(user.is_active)

    def test_update_user(self) -> None:
        User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )
        user = User.objects.last()

        self.client.force_login(user)
        response = self.client.get(reverse('user_update',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'first_name': 'Taika',
                'last_name': 'Waititi',
                'username': 'Wiago',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        user.refresh_from_db()
        self.assertEqual(user.username, 'Wiago')
        self.assertEqual(user.first_name, 'Taika')
        self.assertEqual(user.last_name, 'Waititi')
        self.assertTrue(user.check_password('123qwe!@#'))

    def test_delete_user(self) -> None:
        User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )
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
        self.assertEqual(User.objects.count(), 0)
