import json

from django.contrib.messages.storage.cookie import CookieStorage
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class IndexTestCase(TestCase):
    """
    Test case for homepage, log in and sign up pages,
    UserLogInView and UserLogOutView.
    """
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

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

        user = User.objects.last()
        response = self.client.post(
            reverse_lazy('login'),
            {
                'username': user.username,
                'password': user.password,
            }
        )
        self.assertTrue(user.is_authenticated)
        # messages_list = CookieStorage(response)._decode(
        #     response.cookies['messages'].value
        # )
        # self.assertEqual(
        #     str(messages_list[0]),
        #     _('You are logged in')
        # )

        response = self.client.post(reverse_lazy('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('index'))

        # self.assertFalse(user.is_authenticated)

        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('You are logged out')
        )


class LoginMixinTestCase(TestCase):
    fixtures = ['time.json',
                'users.json',
                'statuses.json',
                'labels.json',
                'tasks.json']

    def setUP(self) -> None:
        self.client = Client()

    def test_access_without_login(self) -> None:
        user = User.objects.last()
        response = self.client.get(reverse('user_update',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages_list = CookieStorage(response)._decode(
            response.cookies['messages'].value
        )
        self.assertEqual(
            str(messages_list[0]),
            _('You are not logged in! Please log in.')
        )


def get_fixture_content(file_path):
    with open(f'task_manager/fixtures/{file_path}', 'r') as input:
        return json.load(input)
