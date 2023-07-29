import json

from django.test import Client, TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class IndexTestCase(TestCase):
    """
    Test case for homepage, log in and sign up pages,
    UserLogInView and UserLogOutView.
    """
    def setUP(self) -> None:
        self.client = Client()

    def test_index_view(self) -> None:
        response = self.client.get(reverse_lazy('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')
        self.assertContains(response, _('Task Manager'), status_code=200)
        self.assertContains(response, _('Log In'), status_code=200)
        self.assertContains(response, _('Sign Up'), status_code=200)
        self.assertContains(response, _('Get started'), status_code=200)

    def test_signup_view(self):
        response = self.client.get(reverse_lazy('user_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')
        self.assertContains(response, _('Task Manager'), status_code=200)
        self.assertContains(response, _('Log In'), status_code=200)
        self.assertContains(response, _('Sign Up'), status_code=200)
        self.assertContains(response, _('Register'), status_code=200)

    def test_login_view(self):
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')
        self.assertContains(response, _('Task Manager'), status_code=200)
        self.assertContains(response, _('Log In'), status_code=200)
        self.assertContains(response, _('Sign Up'), status_code=200)
        self.assertContains(response, _('Enter'), status_code=200)

    def test_login_logout_user(self) -> None:
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

        user = User.objects.create(
            first_name='Taika',
            last_name='Waititi',
            username='Viago',
            password='123qwe!@#',
        )
        response = self.client.post(
            reverse_lazy('login'),
            {
                'username': user.username,
                'password': user.password,
            }
        )
        self.assertTrue(user.is_authenticated)

        response = self.client.post(reverse_lazy('logout'), user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('index'))


def get_fixture_content(file_path):
    with open(f'task_manager/fixtures/{file_path}', 'r') as input:
        return json.load(input)