from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from flip_cards_app.views import MenuMixin
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(MenuMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('index')


class RegisterUser(MenuMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:thanks')


class ThanksForRegistrView(MenuMixin, TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}
