from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthenticationLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/route_search/find_rout_form/'


class AuthenticationLogoutView(LogoutView):
    """Выйти из учетной записи"""
    template_name = 'form_template.html'

    def get_success_url(self):
        return '/'
