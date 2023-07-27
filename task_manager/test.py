from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexTestCase(TestCase):

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

    def test_logout_view(self):
        response = self.client.get(reverse_lazy('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('index'))
