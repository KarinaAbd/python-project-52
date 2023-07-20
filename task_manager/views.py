from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLogInView(LoginView):
    template_name = 'login.html'
    extra_context = {
        'button_text': _('Enter')
    }
    next_page = reverse_lazy('index')
    success_message = _('You are logged in')

    # Флеш сообщения о логине и разлогиниванию не появляются, почему????
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.info(self.request, self.success_message)
            redirect_to = self.get_default_redirect_url()
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class UserLogOutView(LogoutView, SuccessMessageMixin):
    next_page = reverse_lazy('index')
    success_message = _('You are logged out')
